from django.contrib import admin

from .models import Organization, User, Task


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'organization')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('organization',)
    ordering = ('username',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'organization', 'assigned_to', 'completed', 'priority', 'deadline_datetime_with_tz',
                    'created_at')
    search_fields = ('title', 'description')
    list_filter = ('completed', 'organization', 'assigned_to')
    ordering = ('-priority', 'deadline_datetime_with_tz')
    date_hierarchy = 'deadline_datetime_with_tz'
    raw_id_fields = ('assigned_to',)
