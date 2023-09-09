from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser',  'linkedin', 'alternative_email', 'registration_no', 'phone_number', 'year_of_study', 'leadership_role')
    list_filter = ('is_staff', 'is_superuser', 'leadership_role')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'alternative_email', 'linkedin', 'registration_no', 'phone_number', 'year_of_study', 'leadership_role', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser', 'linkedin', 'profile_image', 'alternative_email', 'registration_no', 'phone_number', 'year_of_study', 'leadership_role'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
