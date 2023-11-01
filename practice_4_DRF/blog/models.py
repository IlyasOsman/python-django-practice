from django.db import models
from autoslug import AutoSlugField
import uuid
import os
from django.conf import settings


def blog_image_file_path(instance, filename):
    """Generate file path for new blog image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("blog", filename)


class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    cover_image = models.ImageField(
        upload_to=blog_image_file_path, null=True, blank=True
    )
    authors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="posted_blogs",
        blank=True,
        verbose_name="Authors of the Blog",
    )
    is_project = models.BooleanField(default=False, verbose_name="Is Project")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from="title", unique=True, blank=True)

    def __str__(self):
        return self.title
