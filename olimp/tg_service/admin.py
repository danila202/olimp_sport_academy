from django.contrib import admin

from .models import Children, Parents, CustomUser, SubscriptionType,Employee,\
    TypeSport, Group, Schedule, GroupSchedule, Subscription, Visitation


@admin.register(Children)
class AdminChildren(admin.ModelAdmin):
    list_display = [
        'id','name', 'surname', 'patronymic',
        'mobile_phone', 'birthdate', 'parent_id'
    ]

@admin.register(CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    fields = ['username', 'password', 'is_parent', 'is_child']
    list_display = ['id', 'username', 'password', 'is_parent', 'is_child']


@admin.register(Parents)
class AdminParent(admin.ModelAdmin):
    list_display = ['id', 'name', 'surname', 'patronymic', 'mobile_phone']

@admin.register(Subscription)
class AdminSubscription(admin.ModelAdmin):
    list_display = ['conclusion_date', 'child', 'parent','group']

@admin.register(Visitation)
class AdminVisitation(admin.ModelAdmin):
    list_display = ['date', 'time_of_arrival', 'subscription']

admin.site.register(SubscriptionType)
admin.site.register(Employee)
admin.site.register(TypeSport)
admin.site.register(Group)
admin.site.register(Schedule)
admin.site.register(GroupSchedule)


