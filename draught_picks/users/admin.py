from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import DraughtPicksUser


class DraughtPicksUserCreateForm(UserCreationForm):
    """
    This class creates a form for the user
    """
    class Meta(UserCreationForm.Meta):
        """
        This exposes the fields needed for user creation
        """
        model = DraughtPicksUser
        fields = UserCreationForm.Meta.fields


class DraughtPicksUserChangeForm(UserChangeForm):
    """
    This class changes the user form
    """
    class Meta(UserChangeForm):
        """
        This exposes the fields needed for user change form
        """
        model = DraughtPicksUser
        fields = UserChangeForm.Meta.fields


class DraughtPicksUserAdmin(UserAdmin):
    """
    This class creates the user admin
    """
    add_form = DraughtPicksUserCreateForm
    form = DraughtPicksUserChangeForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                     'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(DraughtPicksUser, DraughtPicksUserAdmin)
