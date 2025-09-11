from django.contrib import admin

from .models import Organization, Task, User


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at',)
    # filter_horizontal = ('users', 'tasks')
    fieldsets = (
        (None, {'fields': ('name',)}),
        (
            'Timestamps',
            {
                'fields': ('created_at',),
                'classes': ('collapse',),
            },
        ),
        # ('Relations', {
        #     'fields': ('users', 'tasks'),
        #     'classes': ('collapse',),
        # }),
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'organization')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'organization')
    ordering = ('username',)
    # filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'organization')}),
        (
            'Permissions',
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                'classes': ('collapse',),
            },
        ),
        (
            'Important dates',
            {
                'fields': ('last_login', 'date_joined'),
                'classes': ('collapse',),
            },
        ),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
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
    readonly_fields = ('created_at', 'deadline_datetime_with_tz')
    date_hierarchy = 'created_at'
    autocomplete_fields = ('assigned_to', 'organization')
