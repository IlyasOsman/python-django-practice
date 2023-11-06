from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = (
            "pk",
            "title",
            "description",
            "cover_image",
            "slug",
            "is_project",
            "created_at",
            "updated_at",
            "authors",
        )
