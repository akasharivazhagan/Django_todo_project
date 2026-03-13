from django.contrib import admin
from django.contrib.auth.models import User,Group
from tasks.models import Task


class TaskInline(admin.TabularInline):

    model = Task
    extra = 0


class CustomUserAdmin(admin.ModelAdmin):

    inlines = [TaskInline]


admin.site.unregister(User) 
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)