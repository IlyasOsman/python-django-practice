from django.db import models
from autoslug import AutoSlugField
import uuid
import os
from authentication.models import BlogAuthor


def blogs_image_file_path(instance, filename):
    """Generate file path for new blog image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("blogs", filename)


class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    cover_image = models.ImageField(
        upload_to=blogs_image_file_path, null=True, blank=True
    )
    authors = models.ManyToManyField(
        BlogAuthor,
        related_name="blogs_authored",
        blank=True,
        verbose_name="Authors of the Blog",
    )
    is_project = models.BooleanField(default=False, verbose_name="Is Project")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from="title", unique=True, blank=True)

    def __str__(self):
        return self.title
