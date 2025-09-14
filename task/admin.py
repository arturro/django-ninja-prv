from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
    list_display = ('title', 'assigned_to', 'organization', 'completed', 'priority')
    search_fields = ('title', 'description', 'assigned_to__username', 'organization__name')
    list_filter = ('completed', 'priority', 'organization')
    ordering = ('-id',)
    fieldsets = (
        (None, {'fields': ('title', 'description', 'priority', 'deadline_datetime_with_tz')}),
        ('Assignment', {'fields': ('assigned_to', 'organization')}),
        (
            'Status',
            {
                'fields': ('completed',),
                'classes': ('collapse',),
            },
        ),
    )
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    autocomplete_fields = ('assigned_to', 'organization')
