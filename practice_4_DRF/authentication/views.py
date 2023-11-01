from rest_framework import generics, viewsets, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserListSerializer,
    LeadershipUserSerializer,
    UserProfileUpdateSerializer,
    PasswordChangeSerializer,
    EmailVerificationSerializer,
    ForgotPasswordSerializer,
    SetNewPasswordSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from django.db.models import Case, Value, When, IntegerField

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import redirect

import jwt
from django.conf import settings

from .utils import Util

from django.views.generic import TemplateView

from django.shortcuts import render

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.permissions import AllowAny
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework.throttling import SimpleRateThrottle

from django.core.cache import cache


class UserLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Check if the user has already requested a verification email.
        user = User.objects.get(username=request.data["username"])
        cache_key = f"verification_email_requested_{user.email}"

        # Prevent unverified users from logging in
        if not user.is_verified:
            # check if they already email verification is sent to them
            if cache.get(cache_key):
                return Response(
                    {"message": "You must verify your email before logging in."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data["username"])
            if not user.is_verified:
                current_site = get_current_site(request)
                relative_link = reverse("verify-email")
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                absurl = f"https://{current_site.domain}{relative_link}?token={token}"

                email_body = render_to_string(
                    "email_verification.html",
                    {
                        "user": user,
                        "absurl": absurl,
                    },
                )

                email_subject = "Verify your email"
                to_email = user.email
                email_plain_text_body = strip_tags(email_body)

                data = EmailMultiAlternatives(
                    subject=email_subject,
                    body=email_plain_text_body,
                    from_email=None,
                    to=[to_email],
                )

                data.attach_alternative(email_body, "text/html")

                Util.send_email(data)

                # Set the cache to indicate that a verification email has been sent.
                cache.set(cache_key, True, timeout=60 * 60)

                return Response(
                    {"message": "A verification email has been sent."},
                    status=status.HTTP_200_OK,
                )

        return response


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        refresh = RefreshToken.for_user(user)

        # Create a verification token and send it via email
        token = str(refresh.access_token)
        current_site = get_current_site(request)
        relative_link = reverse("verify-email")
        absurl = f"http://{current_site.domain}{relative_link}?token={token}"

        email_body = render_to_string(
            "email_verification.html",
            {
                "user": user,
                "absurl": absurl,
            },
        )

        # Create an EmailMultiAlternatives instance
        email_subject = "Verify your email"
        to_email = user.email

        # Remove HTML tags from email_html_body to get plain text content
        email_plain_text_body = strip_tags(email_body)

        data = EmailMultiAlternatives(
            subject=email_subject,
            body=email_plain_text_body,
            from_email=None,
            to=[to_email],
        )

        # Attach the HTML content to the email
        data.attach_alternative(email_body, "text/html")

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(TemplateView):
    serializer_class = EmailVerificationSerializer
    template_name = "authentication/verification_response.html"

    def get(self, request):
        context = {}
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                context["verification_status"] = "Successfully activated"
            # return Response(
            #     {"email": "Successfully activated"}, status=status.HTTP_200_OK
            else:
                context["verification_status"] = "Already verified"

        except jwt.ExpiredSignatureError as identifier:
            # return Response(
            #     {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            # )
            context["verification_status"] = "Activation Expired"
        except jwt.exceptions.DecodeError as identifier:
            # return Response(
            #     {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            # )
            context["verification_status"] = "Invalid token"
        return render(request, self.template_name, context)


class LeadershipUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeadershipUserSerializer

    def get_queryset(self):
        # Get the queryset and order it based on the custom order
        queryset = User.objects.exclude(leadership_role__isnull=True).order_by(
            Case(
                *[
                    When(leadership_role=choice[0], then=Value(order))
                    for order, choice in enumerate(User.LEADERSHIP_CHOICES)
                ],
                default=Value(len(User.LEADERSHIP_CHOICES)),
                output_field=IntegerField(),
            )
        )

        return queryset


class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by("first_name", "last_name")
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
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")
            confirm_new_password = serializer.validated_data.get("confirm_new_password")

            if not user.check_password(old_password):
                return Response(
                    {"detail": "Old password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if new_password != confirm_new_password:
                return Response(
                    {"detail": "New passwords do not match."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()
            return Response(
                {"detail": "Password successfully changed."}, status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileImageView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def update_profile_image(self, user, image):
        user.profile_image = image
        user.save()
        return user.profile_image.url

    def upload_image(self, request):
        serializer = UserProfileUpdateSerializer(
            request.user, data=request.data, partial=True
        )

        if serializer.is_valid():
            # Check if the 'profile_image' key is in the request data
            if "profile_image" in request.data:
                image = request.data["profile_image"]
                self.update_profile_image(request.user, image)

            return Response(
                {
                    "profile_image": request.user.profile_image.url,
                    "detail": "Profile image updated successfully.",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def remove_image(self, request):
        user = request.user
        if user.profile_image:
            user.profile_image.delete()
            user.profile_image = None
            user.save()
            return Response(
                {"detail": "Profile image removed successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "No profile image to remove."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get("email", "")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "No user account associated with this email address."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        # current_site = get_current_site(request=request).domain
        current_site = "localhost:5173"
        relativeLink = reverse(
            "password-reset-confirm", kwargs={"uidb64": uidb64, "token": token}
        )

        absurl = "http://" + current_site + relativeLink

        email_subject = "Password Reset Request"
        email_body = render_to_string(
            "password_reset_email.html", {"absurl": absurl, "user": user}
        )
        email_plain_text_body = strip_tags(email_body)
        to_email = user.email

        # Check the cache to see if the user has already requested a password reset email within the past hour.
        cache_key = f"password_reset_email_requested_{user.email}"
        if cache.get(cache_key):
            return Response(
                {
                    "detail": "You have already requested a password reset email. Please check your email."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = EmailMultiAlternatives(
            subject=email_subject,
            body=email_plain_text_body,
            from_email=None,
            to=[to_email],
        )

        data.attach_alternative(email_body, "text/html")

        Util.send_email(data)

        # Update the cache with the user's email address and a timeout of 1 hour (in seconds).
        cache.set(cache_key, True, 3600)

        return Response(
            {"detail": "Check your email for a link to reset your password."},
            status=status.HTTP_200_OK,
        )


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
                )

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"error": "Invalid user or token."}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Token and user are valid."}, status=status.HTTP_200_OK
        )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )
