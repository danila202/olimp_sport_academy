from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Children, Parents, Subscriptions, CustomUser


@admin.register(Children)
class AdminChildren(admin.ModelAdmin):
    list_display = [
        'name', 'surname', 'patronymic',
        'mobile_phone', 'birthdate', 'parent_id'
    ]


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_parent', 'is_child'),
        }),
    )
    list_display = ['username', 'password', 'is_parent', 'is_child']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Parents)
admin.site.register(Subscriptions)