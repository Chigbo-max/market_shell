from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class CustomUserAdmin(UserAdmin):
    model = User

    add_fieldsets = (
        ('Add User', {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name',
                'password1', 'password2', 'city', 'state', 'phone',
                'address', 'is_active'
            ),
        }),
    )

    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'city', 'state', 'phone', 'address')}),
    #     ('Permissions', {
    #         'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
    #     }),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    # )
    #
    # def get_fieldsets(self, request, obj=None):
    #     if not obj:
    #         return self.add_fieldsets
    #     return super().get_fieldsets(request, obj)
    #
    # def get_form(self, request, obj=None, **kwargs):
    #     if obj is None:
    #         kwargs['form'] = self.add_form
    #     else:
    #         kwargs['form'] = self.form
    #     return super().get_form(request, obj, **kwargs)
    #
    # list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    # search_fields = ('username', 'email', 'first_name', 'last_name')
    # ordering = ('username',)

admin.site.register(User, CustomUserAdmin)