from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import DraughtPicksUser


class DraughtPicksUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = DraughtPicksUser
        fields = UserCreationForm.Meta.fields


class DraughtPicksUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = DraughtPicksUser
        fields = UserChangeForm.Meta.fields


class DraughtPicksUserAdmin(UserAdmin):
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
