from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    UserProfileImage,
    City,
    Plan,
    PostalCode,
    Category,
    PlanJoiningRequest,
)
from .forms import AccountUpdateForm, AccountCreationForm
from django.utils.translation import ugettext_lazy as _


class UserAdmin(UserAdmin):
    form = AccountUpdateForm
    add_form = AccountCreationForm

    list_per_page = 10
    list_display = [
        "pk",
        "email",
        "username",
    ]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "full_name",
                    "username",
                    "profile_image",
                    "date_of_birth",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "full_name",
                    "email",
                    "password1",
                    "password2",
                    "profile_image",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.save()
        return instance


class UserProfileImageAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "user"]


class CityAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "city"]


class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "category_name"]


class PlanAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "title", "user", "plan_datetime"]


class PostalCodeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "city", "postal_code"]


class PlanJoiningRequestAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "user", "plan", "status"]


admin.site.register(User, UserAdmin)
admin.site.register(UserProfileImage, UserProfileImageAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(PostalCode, PostalCodeAdmin)
admin.site.register(PlanJoiningRequest, PlanJoiningRequestAdmin)
