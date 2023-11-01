from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Blog
        fields = "__all__"
