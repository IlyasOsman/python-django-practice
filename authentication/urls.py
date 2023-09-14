from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import UserRegistrationView, UserLoginView, LeadershipUserViewSet, UserListView, UserProfileView, UserDetailView, UserProfileImageView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('leaders/', LeadershipUserViewSet.as_view({'get': 'list'}), name='leaders'),
    path('members/', UserListView.as_view(), name='members'),
    path('members/<int:pk>/', UserDetailView.as_view(), name='members_detail'),
    path('profile/', UserProfileView.as_view({'get': 'retrieve', 'patch': 'update'}), name='profile'),
    path('profile/update_image/', UserProfileImageView.as_view({'post': 'update_image'}), name='update_profile_image'),
    path('profile/change_password/', UserProfileView.as_view({'post': 'change_password'}), name='change_password'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)