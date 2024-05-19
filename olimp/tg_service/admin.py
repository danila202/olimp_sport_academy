from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Children, Parents, Subscriptions, CustomUser


@admin.register(Children)
class AdminChildren(admin.ModelAdmin):
    list_display = [
        'name', 'surname', 'patronymic',
        'mobile_phone', 'birthdate', 'parent_id'
    ]

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    fields = ['username', 'password', 'is_parent', 'is_child']
    list_display = ['id', 'username', 'password', 'is_parent', 'is_child']



admin.site.register(Parents)
admin.site.register(Subscriptions)