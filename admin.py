from django.contrib import admin
from .models import Course, Application

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'duration', 'is_active')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'age', 'course', 'status', 'created_at')
    list_filter = ('status', 'course', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone')
    list_editable = ('status', 'age')
