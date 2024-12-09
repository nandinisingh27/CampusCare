
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default =False)
class Student(models.Model):
        user  = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
        hostel_name = models.CharField(max_length=50)
        room_number = models.IntegerField()
        Department = models.CharField(max_length=50)
        gender = models.CharField(max_length=10)
        address = models.CharField(max_length=80)
        image = models.ImageField(upload_to='images/')
        is_deleted = models.BooleanField(default = False)    


        
class Faculty(models.Model):
    user  = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    experience = models.IntegerField()
    qualification = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    gender = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images/')
    is_deleted = models.BooleanField(default =False)
    
    
class Dropdown(models.Model):
    key = models.CharField(max_length=10)
    value = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,blank = True,related_name='children')

    
class Navbar(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255) 
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,blank = True,related_name='children')
    position = models.IntegerField(default=0)
    icon = models.CharField(max_length=255)
    is_parent = models.BooleanField(default = False)
    role = models.ForeignKey(Dropdown,on_delete = models.SET_NULL,null = True)
    
class UserRole(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null = True)
    role= models.ForeignKey(Dropdown,on_delete = models.SET_NULL,null =True)
    is_deleted = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    date = models.DateTimeField(default=timezone.now)
    
class GrievanceAdded(models.Model):
    user= models.ForeignKey(User,on_delete=models.SET_NULL,null =True)
    description = models.TextField()
    category = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null =True,related_name='category+')
    images = models.ImageField(upload_to= 'grievance_images/')
    title = models.CharField(max_length=255)
    status = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null =True, related_name='status+')
    date = models.DateTimeField(default = timezone.now)   

class ManageGrievance(models.Model):
    grievance = models.ForeignKey(GrievanceAdded,on_delete=models.SET_NULL,null = True)
    user_role = models.ForeignKey(UserRole,on_delete=models.SET_NULL,null =True)
    date = models.DateTimeField(default = timezone.now)
    status = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null = True)
    is_closed = models.BooleanField(default = 0)
    reason = models.TextField(blank=True,default=None,null = True)

class ActionRole(models.Model):
    action = models.ForeignKey(Dropdown,on_delete=models.SET_NULL , null = True,related_name='action+')
    ToBeShown = models.ForeignKey(Dropdown,on_delete = models.SET_NULL,null =True, related_name='to+')
    user = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null = True, related_name='from+')