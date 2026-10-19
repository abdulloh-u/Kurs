from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from courses.views import course_list, course_detail
from applications.views import apply_course
from accounts.views import user_profile
from applications.admin_views import admin_dashboard, update_application_status, delete_application, export_applications_csv
from courses.admin_views import admin_course_list, admin_course_add, admin_course_edit, admin_course_delete
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('courses/', course_list, name='course_list'),
    path('courses/<slug:slug>/', course_detail, name='course_detail'),
    path('apply/', apply_course, name='apply_course'),
    path('profile/', user_profile, name='user_profile'),
    
    # Arizalarni boshqarish (Admin)
    path('custom-admin/', admin_dashboard, name='admin_dashboard'),
    path('custom-admin/update-status/<int:app_id>/', update_application_status, name='update_application_status'),
    path('custom-admin/delete/<int:app_id>/', delete_application, name='delete_application'),
    path('custom-admin/export-csv/', export_applications_csv, name='export_applications_csv'),

    # Kurslarni boshqarish (Admin)
    path('custom-admin/courses/', admin_course_list, name='admin_course_list'),
    path('custom-admin/courses/add/', admin_course_add, name='admin_course_add'),
    path('custom-admin/courses/edit/<int:course_id>/', admin_course_edit, name='admin_course_edit'),
    path('custom-admin/courses/delete/<int:course_id>/', admin_course_delete, name='admin_course_delete'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
