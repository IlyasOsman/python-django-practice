from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import UserRegistrationView, UserLoginView, LeadershipUserViewSet, UserListView, UserProfileView

import os
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('leaders/', LeadershipUserViewSet.as_view({'get': 'list'}), name='leaders'),
    path('members/', UserListView.as_view(), name='members'),
    path('profile/', UserProfileView.as_view({'get': 'retrieve', 'put': 'update'}), name='profile'), 
    path('profile/change_password/', UserProfileView.as_view({'post': 'change_password'}), name='change_password'),
    path('profile/update_image/', UserProfileView.as_view({'patch': 'update_image'}), name='update_profile_image'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=os.path.join(settings.BASE_DIR, 'media'))