from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, State
# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['id','username','date_joined','is_superuser','is_petowner', 'is_adopter']
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'state', 'city', 'zipcode', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions', 'is_petowner', 'is_adopter')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'state', 'city', 'zipcode'),
        }),
    )

    admin.site.register(State)