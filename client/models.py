from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Substr
from django.db.models.signals import post_save
from django.dispatch import receiver

def upload_to(instance, filename):
    return "users/{}/{}".format(instance.id, filename)

class UserSiteRole(models.Model):
    name = models.TextField()

class Course(models.Model):
    code = models.TextField()
    name = models.TextField()

    def __str__(self):
        return "{}".format(self.code)

class User(AbstractUser):
    hearts = models.IntegerField(default=0)
    hearted_users = models.ManyToManyField("User", related_name="hearted_by", blank=True)
    is_moderator = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    site_roles = models.ManyToManyField(UserSiteRole, related_name="users", blank=True)
    courses = models.ManyToManyField(Course, related_name="courses", blank=True)
    # profile
    about = HTMLField(blank=True)
    photo = models.URLField(blank=True)
    resume = models.URLField(blank=True)

    def __str__(self):
        return "{}".format(self.username)

class Project(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.TextField()  # what is the name of the project
    hearts = models.IntegerField(default=0)
    description = models.TextField()  # rich-text description
    category = models.ForeignKey("ProjectCategory", on_delete=models.CASCADE, related_name="projects")
    members = models.ManyToManyField(User, related_name="member_projects")
    leaders = models.ManyToManyField(User, related_name="leader_projects")
    hearted_by = models.ManyToManyField(User, related_name="hearted_projects", blank=True)
    tags = models.ManyToManyField("ProjectTag", related_name="projects", blank=True)
    
    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return "{}".format(self.name)

class ProjectCategory(models.Model):
    name = models.TextField()

    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"

    def __str__(self):
        return "{}".format(self.name)

class ProjectTag(models.Model):
    name = models.TextField()

    class Meta:
        verbose_name = "Project Tag"
        verbose_name_plural = "Project Tags"

    def __str__(self):
        return "{}".format(self.name)

class ProjectJoinRequest(models.Model):
    request = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="join_requests", blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="join_requests", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return "{} : {}".format(self.user, self.project)

    class Meta:
        verbose_name = "Project Join Request"
        verbose_name_plural = "Project Join Requests"

class ProjectComment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="comments", blank=True, null=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    anonymous = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = "Project Comment"
        verbose_name_plural = "Project Comments"

    def __str__(self):
        return "{} ...".format(self.comment[0:20])

class ProjectPost(models.Model):
    post = models.TextField()
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_posts", blank=True, null=True)
    private = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = "Project Post"
        verbose_name_plural = "Project Posts"

    def __str__(self):
        return "{} ...".format(self.post[0:20])

class Message(models.Model):
    # which user sent the message
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_messages")
    # the associated data with the message
    body = HTMLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_join_request = models.BooleanField(default=False)
    in_trash = models.BooleanField(default=False)
    is_unread = models.BooleanField(default=True)
    is_seen = models.BooleanField(default=False)
    # which conversation does the message belong to? (this includes receivers)
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, related_name="messages", null=True)

    class Meta:
       ordering = ['timestamp']

class Conversation(models.Model):
    conversants = models.ManyToManyField(User, related_name="conversations")
    my_unread_count = models.IntegerField(default=0)
    their_unread_count = models.IntegerField(default=0)
    # is equal to the timestamp of the last message (helps order in conversation list view)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
       ordering = ['-timestamp']

class Post(models.Model):
    posted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts", blank=True, null=True
    )
    cover_image = models.URLField(blank=True)
    title = models.TextField(max_length=200, null=True)
    body = HTMLField()
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="posts", blank=True, null=True)
    is_private = models.BooleanField(default=False)
    is_site = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return "{} ...".format(self.body[0:20])
