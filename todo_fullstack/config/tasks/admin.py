from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'user',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'created_at'
    )

    search_fields = (
        'title',
        'user__username'
    )

    ordering = (
        '-created_at',
    )


admin.site.register(Task, TaskAdmin)