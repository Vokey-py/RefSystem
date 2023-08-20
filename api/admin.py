from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, InvitationCode


class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = ("code", )


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "phoneNumber", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "phoneNumber", "password", "invitation_code_self", "invitation_code_other")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phoneNumber", "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(InvitationCode, InvitationCodeAdmin)
