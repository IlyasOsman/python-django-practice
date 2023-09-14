from django.core.exceptions import ValidationError
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserListSerializer,
    LeadershipUserSerializer,
    UserProfileUpdateSerializer,
    PasswordChangeSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from PIL import Image

class UserLoginView(TokenObtainPairView):
    username_field = 'email'

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class LeadershipUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.exclude(leadership_role__isnull=True)
    serializer_class = LeadershipUserSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

class UserProfileView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserProfileUpdateSerializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def change_password(self, request):
        user = self.get_object()
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            confirm_new_password = serializer.validated_data.get('confirm_new_password')

            if not user.check_password(old_password):
                return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_new_password:
                return Response({'detail': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password successfully changed.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileImageView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def get_object(self):
        return self.request.user

    def update_image(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # Handle profile image update separately
            profile_image = request.data.get('profile_image')
            if profile_image:
                # Validate the file format and size
                if not profile_image.name.endswith(('.jpg', '.jpeg', '.png')):
                    return Response({'detail': 'Only JPG, JPEG and PNG images are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

                max_size = 5 * 1024 * 1024  # 5 MB
                if profile_image.size > max_size:
                    return Response({'detail': 'Image file size is too large.'}, status=status.HTTP_400_BAD_REQUEST)

                # Read and process the image (e.g., resize it)
                with Image.open(profile_image) as img:
                    img.thumbnail((300, 300))  # Resize the image

                    # Create an in-memory file to save the processed image
                    output = BytesIO()
                    img.save(output, format='JPEG')
                    output.seek(0)

                    # Create an InMemoryUploadedFile with the processed data and the unique filename
                    processed_file = InMemoryUploadedFile(
                        output, None, user.profile_image.name, 'image/jpeg', output.tell(), None
                    )

                # Save the processed image to the user's profile_image field
                user.profile_image = processed_file
                user.save()

            return Response({'detail': 'Profile image updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)