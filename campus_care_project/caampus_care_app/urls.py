from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('student_register/',views.student_register),
    path('faculty_register/',views.faculty_register),
    path('login/',views.login_user),
    path('logout/',views.logout_user),
    path('list_items/',views.list_items_dropdown),
    path('profile/',views.profile_det),
    path('list_faculty/',views.list_faculty),
    path('navbar/',views.navbar),
    path('list_roles/',views.list_roles),
    path('change_role/',views.change_role),
    path('assign_roles/',views.assign_roles),
    path('add_grievance/',views.add_grievance),
    path('list_grievance/',views.list_grievance),
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

