from rest_framework import generics, permissions
from .models import Blog
from .serializers import BlogSerializer
from .permissions import IsBlogAuthor
from rest_framework.exceptions import PermissionDenied


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_member:
            serializer.save(authors=[user])
        else:
            raise PermissionDenied("You must be a member to create a blog.")


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "slug"

    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()

        # Check if the user is the author of the blog
        if user not in instance.authors.all():
            raise PermissionDenied("You are not the author of this blog.")

        # Get the new cover image
        new_cover_image = self.request.data.get("cover_image")

        if new_cover_image:
            # Remove the existing cover image from storage
            instance.cover_image.delete(save=False)

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if user in instance.authors.all():
            # Remove the cover_image from storage
            instance.cover_image.delete(save=False)
            instance.delete()
        else:
            raise PermissionDenied("You are not the author of this blog.")
