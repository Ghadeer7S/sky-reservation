from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Exists, OuterRef
from .models import User
from users.models import Profile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'has_profile')  # ✅ عمود جديد
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(has_profile_exists=Exists(
            Profile.objects.filter(user=OuterRef('pk'))
        ))

    def has_profile(self, obj):
        return obj.has_profile_exists

    has_profile.boolean = True