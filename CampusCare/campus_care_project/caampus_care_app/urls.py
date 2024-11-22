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
    path('list_faculty/',views.list_faculty)
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

