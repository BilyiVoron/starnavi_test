from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from users.forms import UserChangeForm, UserCreationForm
from allauth.account.admin import EmailAddressAdmin
from allauth.account.models import EmailAddress


User = get_user_model()


class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ["username", "is_superuser", "email"]
    search_fields = ["username"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MyEmailAddressAdmin(EmailAddressAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TokenAdmin(admin.ModelAdmin):
    list_display = ("key", "user", "created")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(User, UserAdmin)

admin.site.unregister(Token)
admin.site.register(Token, TokenAdmin)

admin.site.unregister(EmailAddress)
admin.site.register(EmailAddress, MyEmailAddressAdmin)
