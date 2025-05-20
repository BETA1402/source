from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class Users(admin.ModelAdmin):
    list_filter = ('id','playedMinutes')
    search_fields = ('id','phoneNumber')
    list_display = ('id','name','phoneNumber','uuid')
    readonly_fields = ('uuid',)  # Optional: prevent editing in admin< 

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"
# @admin.register(System)
@admin.action(description="Mark selected stories as published")
def test(modeladmin, request, queryset):
    queryset.update(is_available=True)

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('is_available','hourlyRate','systemName')
    list_filter = ('is_available',)
    search_fields = ('is_available',)
    actions = [test]
    class Meta:
        verbose_name = 'System'
        verbose_name_plural = "Systems"
    def test():
        pass

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('startTime','endTime','duration')
    list_filter = ('startTime','endTime','duration')
    search_fields = ('startTime',)
    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = "Teams"
        
@admin.register(PlaySession)
class PlaySessionAdmin(admin.ModelAdmin):
    list_display = ('user','start_time','sesionDuration')
    list_filter = ('user','start_time','sesionDuration')
    search_fields = ('start_time',)
    class Meta:
        verbose_name = 'PlaySession'
        verbose_name_plural = "PlaySessions"

# admin.site.register(Users)
# admin.site.register(SystemAdmin)
# admin.site.register(TeamAdmin)
# admin.site.register(System)
