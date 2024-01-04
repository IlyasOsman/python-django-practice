from django.db import models
from autoslug import AutoSlugField
from authentication.models import User
import uuid
import os


def blogs_image_file_path(instance, filename):
    """Generate file path for new blog image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("blogs", filename)


class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=1000)
    link = models.CharField(max_length=255, null=True)
    cover_image = models.ImageField(
        upload_to=blogs_image_file_path, null=True, blank=True
    )
    is_project = models.BooleanField(default=False, verbose_name="Is Project")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from="title", unique=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="comments", null=True
    )
    comment = models.CharField(max_length=600, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class CommentReply(models.Model):
    reply = models.TextField(max_length=500, blank=True, null=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies", null=True
    )
    replier = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reply


class Upvote(models.Model):
    upvoted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="+"
    )
    post = models.ForeignKey(
        Blog, on_delete=models.CASCADE, null=True, related_name="upvotes"
    )

    class Meta:
        unique_together = [["upvoted_by", "post"]]


class CommentUpvote(models.Model):
    upvoted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="+"
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True, related_name="upvotes"
    )

    class Meta:
        unique_together = [["upvoted_by", "comment"]]


class CommentReplyUpvote(models.Model):
    upvoted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="+"
    )
    reply = models.ForeignKey(
        CommentReply, on_delete=models.CASCADE, null=True, related_name="upvotes"
    )

    class Meta:
        unique_together = [["upvoted_by", "reply"]]
