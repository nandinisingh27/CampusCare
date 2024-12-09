from django.shortcuts import render
import re
from django.db.models import Q
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse
from .models import Faculty
from .models import Student
from .models import Dropdown
from .models import Navbar
from .models import UserRole
from .models import GrievanceAdded
from .models import ManageGrievance
from django.contrib.auth.models import User
from .tasks import increase_variable_after_working_hours

def faculty_register(request):
    user =request.user
    if not user.is_authenticated:
        return JsonResponse({"error":"Unauthorized"},status =401)
    else:
        id = user.id
        user_role =UserRole.objects.filter(user_id =id).filter(is_active=1).values()
        role_id = user_role[0]['role_id']
        if role_id == 29:        
            if request.method=="POST":
                first_name = request.POST['first_name']
                if first_name:
                    if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,29}$",first_name)):
                        return JsonResponse({'error':'Please enter a valid first name'},status =400)
                else:
                        return JsonResponse({'error':'Please enter first name'},status =400)
                        
                last_name = request.POST['last_name']
                email = request.POST['email']
                if User.objects.filter(username = email).exists():
                    return JsonResponse({"error":'Email already exist, Please register with another email'},status =400)
                if  email:
                    if not bool(re.match(r"[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}",email)):
                        return JsonResponse({'error':'Please enter a valid email'},status =400)
                else:
                        return JsonResponse({'error':'Please enter a valid email ID'},status =400)
                address = request.POST['address']
                if not address :
                    return JsonResponse({'error':'Please enter a valid address'},status =400)
                phone_number =request.POST['phone_no']
                if  phone_number :
                    if not bool(re.match(r"^[6-9]{1}[0-9]{9}$",phone_number)):
                        return JsonResponse({'error':'Please enter a valid phone number'},status =400)
                else:
                        return JsonResponse({'error':'Please enter a valid phone number'},status =400)
                if len(request.FILES)!= 0:
                    image = request.FILES['profile_image']
                    if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                        return JsonResponse({'error':'Only jpg, png and jpeg format are allowed!'},status=400)
                else:
                    return JsonResponse({'error':'Please upload a valid image '},status =400)
                password = request.POST['password_1']
                cpassword =  request.POST['password_2']
                if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$",password)):
                    return JsonResponse({'error':'password must  contain at least a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =400)
                if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$",cpassword)):  
                    return JsonResponse({'error':'password must  contain at least a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =400)
                if password != cpassword:
                    return JsonResponse({'error':'Password and confirm password do not match'},status = 400)
                gender = request.POST['gender']
                if  gender :
                    if not bool(re.match(r"^[a-zA-Z]+$",gender)):
                        return JsonResponse({'error':'Please enter valid gender'},status =400)
                else:
                    return JsonResponse({'error':'Please enter valid gender'},status =400)
                qualification = request.POST['qualification']
                if not qualification :
                    return JsonResponse({'error':'Please a enter valid qualification'},status =400)
                experience=request.POST['experience']
                user = User.objects.create_user(first_name= first_name,username=email,last_name=last_name,password = password, is_staff = 1)
                Faculty.objects.create(user=user,experience=experience,qualification=qualification,gender =gender,image = image,address = address)
                lst = Dropdown.objects.filter(key = "FT").values()
                id = lst[0]['id']
                user_det = User.objects.filter(username = email).values()
                user_ID = user_det[0]['id']
                UserRole.objects.create(user_id = user_ID,is_active = 1,role_id = id)
                return JsonResponse({'message':'Faculty account created successfully'},status = 200)
            else:
                return JsonResponse({'message':"Method not allowed"},status =405)
        else:
                return JsonResponse({'error':"You are not allowed to access this page"},status =403)
    
    
    
    
def student_register(request):
    user =request.user
    if not user.is_authenticated:
        return JsonResponse({"error":"Unauthorized"},status =401)
    else:
        id = user.id
        user_role =UserRole.objects.filter(user_id =id).filter(is_active=1).values()
        role_id = user_role[0]['role_id']
        if role_id == 29:        
            if request.method=="POST":
                first_name = request.POST['first_name']
                if  first_name:
                    if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,29}$",first_name)):
                        return JsonResponse({'error':'Please enter a valid first name'},status =400)
                else:
                        return JsonResponse({'error':'Please enter first name'},status =400)
                last_name = request.POST['last_name']
                email = request.POST['email']
                
                if  email :
                    if not bool(re.match(r"[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}",email)):
                        return JsonResponse({'error':'Please enter a valid email'},status =400)
                else:
                    return JsonResponse({'error':'Please enter a valid email ID'},status =400)
                if User.objects.filter(username = email).exists():
                    return JsonResponse({"error":'Email already exist, Please register with another email'},status =400)
                phone_number =request.POST['phone_no']
                if  phone_number :
                    if not bool(re.match(r"^[6-9]{1}[0-9]{9}$",phone_number)):
                        return JsonResponse({'error':'Please enter a valid phone number'},status =400)
                else:
                    return JsonResponse({'error':'Please enter a valid phone number'},status =400)
                if len(request.FILES)!= 0:
                    image = request.FILES['profile_image']
                    if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                        return JsonResponse({'error':'Only jpg, png and jpeg format are allowed!'},status=400)
                branch = request.POST['department']
                if not branch:
                    return JsonResponse({'error':'Please enter a valid branch'},status =400)

                address = request.POST['address']
                if not address:
                    return JsonResponse({'error':'Please enter a valid address'},status =400)
                hostel_name = request.POST['hostel']
                if not hostel_name :
                    return JsonResponse({'error':'Please enter a valid hostel name'},status =400)
                room_number = request.POST['room_no']
                if  room_number:
                    if not bool(re.match(r"^[0-9]{3}$",room_number )):
                        return JsonResponse({'error':'Please enter a valid room number'},status =400)
                else:
                    return JsonResponse({'error':'Please enter a valid room number'},status =400)
                password = request.POST['password_1']
                cpassword =  request.POST['password_2']
                if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$",password)):
                    return JsonResponse({'error':'password must  contain at least a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =400)
                if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$",cpassword)):
                    return JsonResponse({'error':'password must  contain at least a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =400)
                if password != cpassword:
                    return JsonResponse({'error':'Password and confirm password do not match'},status = 400)
                gender = request.POST['gender']
                if not gender :

                    return JsonResponse({'error':'Please enter valid gender'},status =400)
                user = User.objects.create_user(first_name= first_name,username=email,last_name=last_name,password = password)
                Student.objects.create(image= image,user=user,hostel_name=hostel_name,room_number=room_number,address = address,gender=gender,Department =branch)
                lst = Dropdown.objects.filter(key = "S").values()
                id = lst[0]['id']
                user_det = User.objects.filter(username = email).values()
                user_ID = user_det[0]['id']
                UserRole.objects.create(user_id =user_ID , role_id = id,is_active = 1)
                return JsonResponse({'message':'Student account created successfully'},status = 200)
            else:
                return JsonResponse({'message':"Method not allowed"},status =405)
        else:
            return JsonResponse({"error":'You are not allowed to access this page'},status=403)

def role_type_key(user):
    info = User.objects.filter(username=user).values()
    user_id= info[0]['id']
    role_info = UserRole.objects.filter(user_id =  user_id).values_list()
    details =[]
    for i in role_info:
        role_id= i[2]
        role_det = Dropdown.objects.filter(id = role_id).values()
        role = role_det[0]['key']
        val = {
        'role':role,
            'id':role_id
        }
        details.append(val)
    return details

def formatdate(date):
    format = date.strftime("%d/%m/%Y  Time:%H:%M")
    return format

def role_type(user):
    info = User.objects.filter(username=user).values()
    user_role = info[0]['is_staff']
    user_id= info[0]['id']    
    role_info = UserRole.objects.filter(user_id =  user_id).filter(is_deleted =0).values_list()
    details =[]
    for i in role_info:
        role_id= i[2]
        role_det = Dropdown.objects.filter(id = role_id).values()
        role = role_det[0]['value']
        val = {
        'role':role,
            'id':role_id
        }
        details.append(val)
    return details


def gender_type(user):
    info = User.objects.filter(username=user).values()
    user_role = info[0]['is_staff']
    user_id= info[0]['id']
    if user_role == 1:
        role_info = Faculty.objects.filter(user_id =  user_id).values()
        role_ = role_info[0]['gender']
        role_val = Dropdown.objects.filter(key = role_).values()
        gender = role_val[0]['value']
        
        return gender
    else:
        role_info = Student.objects.filter(user_id =  user_id).values()
        role_ = role_info[0]['gender']
        role_val = Dropdown.objects.filter(key = role_).values()
        gender = role_val[0]['value']
        return gender

def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        email = data.get('email')
        password = data.get('password')
        if email is None:
            return JsonResponse({'error': 'Please enter email'}, status=400)
        if password is None:
            return JsonResponse({'error': 'Please enter password'}, status=400)
        if email and password is None:
            return JsonResponse({'error':'Please enter your credentials'},status=400)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            user_info = User.objects.filter(username = user).values()
            user_ID = user_info[0]['id']
            role_det = UserRole.objects.filter(user_id =user_ID).filter(is_active = 1).values()
            role_ID = role_det[0]['role_id']
            state_det = Navbar.objects.filter(role_id =role_ID).filter(position =1).values()
            state = state_det[0]['link']
            return JsonResponse({'message':"Successfully logged in!",'state':state},status =200)
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
def logout_user(request):
    if request.method == "GET":
        user  = request.user
        if user.is_authenticated:
            logout(request)
            return JsonResponse({'message':'Logged out!!'},status = 200)
        else:
            return JsonResponse({'error':'Invalid user'},status = 400)
        
    else:
        return JsonResponse({'error':'Invalid method'},status =405 )
    
def list_items_dropdown(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error':'Unauthorized'},status =401)
        type = request.GET.get('type')
        det = Dropdown.objects.filter(parent_id = type).values()
        details=[]
        for item in det:
            val={
                
                'id':item['id'],
                'key':item['key'],
                'value':item['value']
                }
            details.append(val)
        return JsonResponse({'data':details},status =200)
    else:
        return JsonResponse({'error':"Method not allowed"},status = 405)
    
def profile_det(request):
    if request.method=="GET":
        user = request.user
        
        if not request.user.is_authenticated :
            return JsonResponse({"error":"Unauthorized"},status =401)
        user_det = User.objects.filter(username =user).values()
        _id = user.id
        is_staff = user_det[0]['is_staff']
        user_data= UserRole.objects.filter(user_id = _id).filter(is_active=True).values()
        role_id = user_data[0]['role_id']
        data = Dropdown.objects.filter(id = role_id).values()
        role = data[0]['value']
        gender = gender_type(user)
        userDet = []
        for item in user_det:    
            first_name=item['first_name']
            last_name=item['last_name']
            name = first_name+" "+ last_name
            email=item['username']        
            if is_staff is True:
                fac = Faculty.objects.filter(user_id=_id).values()
                for item in fac:
                    values={
                'name':name,
                'email':email,
                'image':item['image'],
                'experience':item['experience'],
                'qualification':item['qualification'],
                'role':role,
                'gender':gender,
                'address':item['address']
                    }
                userDet.append(values)
            else:
                stud = Student.objects.filter(user_id=_id).values()
                for item in stud:
                    hostel = item['hostel_name']
                    hostel_ = Dropdown.objects.filter(key = hostel).values()
                    host = hostel_[0]['value']
                    dept = item['Department']
                    dept_ = Dropdown.objects.filter(key = dept).values()
                    dept_m = dept_[0]['value']
                    gender_ = item['gender']
                    gender_e = Dropdown.objects.filter(key = gender_).values()
                    gen= gender_e[0]['value']
                    values={
                'name':name,
                'email':email,
                'image':item['image'],
                'hostel':host,
                'room number':item['room_number'],
                'role':role,
                'department':dept_m,
                'gender':gen,
                'address':item['address']
                    }
                userDet.append(values)
        return JsonResponse({'data':userDet},status =200)
    else:
        return JsonResponse({'error':'Method not allowed'},status =405)
    
def list_faculty(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
        user_id = user.id
        user_role = UserRole.objects.filter(user_id = user_id).filter(is_active=1).values()
        role_id = user_role[0]['role_id']
        if role_id == 28:
            details =[]
            fac= User.objects.filter(is_staff =1).values()
            for item in fac:
                id = item['id']
                det = Faculty.objects.filter(user_id = id).values()
                image = det[0]['image']
                exp = det[0]['experience']
                qualification =det[0]['qualification']
                
                user_det = User.objects.filter(id =id).values()
                f_name= user_det[0]['first_name']
                l_name = user_det[0]['last_name']
                name =f_name+" "+l_name
                email = user_det[0]['username']
                role = role_type(email)
                active_roles =[]
                for item in role:
                    vale = item['role']
                    active_roles.append(vale)
                val = {
                    'id':id,
                    'name':name,
                    'email':email,
                    'image':image,
                    'experience':exp,
                    'qualification':qualification,
                    'role':role,
                    'active_roles':active_roles
                }
                details.append(val)
                            
            return JsonResponse({"list":details},status =200)
        else:
            return JsonResponse({'error':"You are not allowed to access this page!"},status = 403)
    else:
        return JsonResponse({'error':'Method not allowed'},status =405)
    
    
def list_roles(request):
    user = request.user
    if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
    id= user.id
    roles_det = UserRole.objects.filter(user_id = id).filter(is_deleted = 0).values()
    
    roles =[]
    for item in roles_det:
        id = item['role_id']
        active = item['is_active']
        role_ = Dropdown.objects.filter(id =id).values()
        val = {
            'id':role_[0]['id'],
            'role': role_[0]['value'],
            'active':active   
        }
        roles.append(val)
    return JsonResponse({'data':roles},status =200)
    
def change_role(request):
    if request.method =="PUT":
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
        user_i = user.id
        data =json.loads(request.body)
        role_id = data.get('role')
        user_det = UserRole.objects.filter(role_id = role_id).values()
        user_id = user_det[0]['user_id']
        user_=UserRole.objects.filter(role_id = role_id).filter(user_id = user_i).update(is_active=1)
        user_1 = UserRole.objects.filter(role_id = role_id).filter(user_id = user_i).values()
        print(user_1)
        USeR=UserRole.objects.filter(user_id = user_i).values().exclude(role_id = role_id).update(is_active = 0)
        USeR_=UserRole.objects.filter(user_id = user_i).exclude(role_id = role_id).values()
        print(USeR_)
        state_list = Navbar.objects.filter(role_id = role_id).filter(title = "Dashboard").values()
        state = state_list[0]['link']
        return JsonResponse({'message':'Role changed successfully!','state':state},status = 200)
    else:
        return JsonResponse({"error":'Method Invalid'},status =405)
    



def navbar(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
        user_id = user.id
        role_det = UserRole.objects.filter(user_id = user_id).filter(is_active = True).values()
        role_id  = role_det[0]['role_id']
        user_det = User.objects.filter(username = user).values()
        user_id = user_det[0]['id']
        items = Navbar.objects.filter(role_id = role_id).values().order_by('position')
        det = []
        for i in items:
            children = []
            is_parent = i['is_parent']
            if is_parent:
                child = i['parent_id']
                child_det = Navbar.objects.filter(id = child).values()
                parent_id = child_det[0]['parent_id']
                parent_ = Navbar.objects.filter(parent_id =parent_id).values().order_by('position')
                for item in parent_:
                    val = {
                        'id':item['id'],
                        'title':item['title'],
                        'icon':item['icon'],
                        'state':item['link']
                        }
                    children.append(val)    
                values = {
                    'id':i['id'],
                    'title':i['title'],
                    'icon':i['icon'],
                    'state':i['link'],
                    'child':children
                    }        
                det.append(values)
            else:
                values = {
                    'id':i['id'],
                    'title':i['title'],
                    'icon':i['icon'],
                    'state':i['link'],
                    'child':children
                    }        
                det.append(values)
                
                
            
        return JsonResponse({"data":det},status =200)
    else:
        return JsonResponse({'error':'Invalid Method'},status =405)
    
def assign_roles(request):
    if request.method == "POST":
        user =request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
        user_det =User.objects.filter(username =user).values()
        user_id = user_det[0]['id']
        user_role = UserRole.objects.filter(user_id = user_id).filter(is_active =1).values()
        rol = user_role[0]['role_id']
        if rol == 28:
                
                data = json.loads(request.body)
                role = data.get('role')
                user_id = data.get('user_id')
                UserRole.objects.create(user_id = user_id , role_id =role)
                
                return JsonResponse({'message':'Role added successfully'},status = 200)
        else:
            return JsonResponse({"error":"You are not allowed to access this page"},status=403)
    elif request.method == "PATCH":
        data  = json.loads(request.body)
        print(data)
        user_d = data.get('user')
        role_id = data.get('role')   
        lst = UserRole.objects.filter(user_id = user_d).filter(role_id= role_id).update(is_deleted = 1)
        return JsonResponse({'message':'Role deleted successfully!'},status =200)
    else:
        return JsonResponse({'error':'Invalid Method'},status =405)

def add_grievance(request):
    if request.method == "POST":
        user =request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
        user_det = User.objects.filter(username = user).values()
        user_id = user_det[0]['id']
        user_role = UserRole.objects.filter(user_id = user_id).filter(is_active =1).values()
        user_role_ID = user_role[0]['id']
        rol = user_role[0]['role_id']
        if rol == 24:
                title = request.POST['title']
                if  title:
                    if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,50}$",title)):
                        return JsonResponse({'error':'Please enter a valid title'},status =400)
                else:
                    return JsonResponse({'error':'Please enter a valid title'},status =400)
                description = request.POST['description']
                if not description:
                    return JsonResponse({'error':'Please enter a valid description'},status =400)
                if len(request.FILES)!= 0:
                    image = request.FILES['image']
                    if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                        return JsonResponse({'error':'Only jpg, png and jpeg format are allowed!'},status=400)
                else:
                    return JsonResponse({'error':'Please upload a valid image '},status =400)
                category = request.POST['category']
                if not category:
                    return JsonResponse({'error':'Please enter a valid category'},status =400)
                grievance = GrievanceAdded.objects.create(user_id = user_id,category_id = category,title =title,description = description,images = image,status_id = 55)
                ManageGrievance.objects.create(grievance=grievance,user_role_id = user_role_ID,status_id =55)
                
                return JsonResponse({'message':'Grievance added successfully!'},status =200)
                    
        else:
                return JsonResponse({"error":'You are not allowed to access this page!'},status =403)
    else:
        return JsonResponse({"error":'Invalid Method'},status = 405)

def list_grievance(request):
    if request.method == "GET":
        user =request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
        user_id = user.id
        user_role = UserRole.objects.filter(user_id = user_id).filter(is_active =1).values()
        role = user_role[0]['role_id']
        details =[]
        
        if role == 24:            
            if not GrievanceAdded.objects.filter(user_id = user_id).exists():
                return JsonResponse({'data':details},status =200)
            user_grievance = GrievanceAdded.objects.filter(user_id = user_id).values().exclude(Q(status_id =57)or Q(status_id =62)or Q(status_id =66)or Q(status_id =70)or Q(status_id =74) )
            for item in user_grievance:
                date = item['date']
                f_date = formatdate(date)
                id  =item['id']
                status=[]
                manage = ManageGrievance.objects.filter(grievance_id =id).order_by('id').values()
                for i in manage:
                    statusID = i['status_id']
                    det = Dropdown.objects.filter(id=statusID).values()
                    if statusID ==56 or statusID ==61 or statusID==65 or statusID==69 or statusID==73:
                        active = True
                    else:
                        active = False
                    vali = det[0]['value']
                    status.append(vali)
                    
                val = {
                    'id':id,
                    'title': item['title'],
                    'description':item['description'],
                    'date':f_date,
                    'image':item['images'],
                    'status':status,
                    'active':active,
                    'message':i['reason']
                }
                details.append(val)
            return JsonResponse({'data':details},status =200)
        elif role == 25:
            user_hostel = Student.objects.filter(hostel_name ="SJ").values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).order_by('status_id').values().exclude(status_id =58)
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']
                    if stat == 55:
                        f_stat = 1
                        message = ""
                    else:
                        f_stat = 0
                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'description':i['description'],
                    'date':f_date,
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'status':f_stat,                    
                    }
                    if stat ==56:
                        message = "Grievance Resolved"
                        val['message']  = message
                    elif stat==59:
                        message = "Grievance forwarded to Admin officer"
                        val['message']  = message
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        
        elif role == 43:
            user_hostel = Student.objects.filter(hostel_name ="GG").values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).order_by('status_id').values().exclude(status_id =58)
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']
                    if stat == 55 :
                        f_stat = 1
                        message = ""
                    else:
                        f_stat = 0
                        
                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'description':i['description'],
                    'date':f_date,
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'status':f_stat,                    
                    }
                    if stat ==56:
                        message = "Grievance Resolved"
                        val['message']  = message
                    elif stat==59:
                        message = "Grievance forwarded to Admin officer"
                        val['message']  = message
                    details.append(val)
                    # increase_variable_after_working_hours.delay(new_data.id)
            return JsonResponse({'data':details},status=200)
        elif role == 44:
            user_hostel = Student.objects.filter(hostel_name ="CG").values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).order_by('status_id').values().exclude(status_id =58)
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']
                    if stat == 55:
                        f_stat = 1
                        message = ""
                    else:
                        f_stat = 0
                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'description':i['description'],
                    'date':f_date,
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'status':f_stat,                    
                    }
                    if stat ==56:
                        message = "Grievance Resolved"
                        val['message']  = message
                    elif stat==59:
                        message = "Grievance forwarded to Admin officer"
                        val['message']  = message
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role == 45:
            user_hostel = Student.objects.filter(hostel_name ="CV").values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).order_by('status_id').values().exclude(status_id =58)
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']
                    if stat == 55:
                        f_stat = 1
                        message = ""
                    else:
                        f_stat = 0
                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'description':i['description'],
                    'date':f_date,
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'status':f_stat,                     
                    }
                    if stat ==56:
                        message = "Grievance Resolved"
                        val['message']  = message
                    elif stat==59:
                        message = "Grievance forwarded to Admin officer"
                        val['message']  = message
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role ==23:
            user_hostel = Student.objects.all().values()    
            for items in user_hostel:
                print(items)
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).filter(Q(status_id = 59) | Q(status_id = 64) |Q(status_id = 68) |Q(status_id = 72) ).order_by('status_id').values()
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']
                    if stat == 55:
                        f_stat = 1
                        # message = ""
                    else:
                        f_stat = 0
                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'description':i['description'],
                    'date':f_date,
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'status':f_stat,                    
                    }
                    if stat ==56:
                        message = "Grievance Resolved"
                        val['message']  = message
                    elif stat==57:
                        message = "Grievance forwarded to Admin officer"
                        val['message']  = message
                    details.append(val)
                    if len(details)==0:
                        return JsonResponse({"data":'No Pending Grievance'},status =200)
                    
            return JsonResponse({'data':details},status=200)
        elif role ==28:
            user_hostel = Student.objects.all().values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =71).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']
                    if stat == 55:
                        f_stat = 1
                        message = ""
                    else:
                        f_stat = 0
                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'description':i['description'],
                    'date':f_date,
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'status':f_stat,                    
                    }
                    if stat ==56:
                        message = "Grievance Resolved"
                        val['message']  = message
                    elif stat==57:
                        message = "Grievance forwarded to Admin officer"
                        val['message']  = message
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role==47:
            user_hostel = Student.objects.filter(hostel_name ="SJ").values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).filter(Q(status_id = 58) | Q(status_id = 63)).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']
                    if stat == 55:
                        f_stat = 1
                    
                    else:
                        f_stat = 0
                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'description':i['description'],
                    'date':f_date,
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'status':f_stat,                    
                    }
                    
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role ==46:
            user_hostel = Student.objects.filter(hostel_name ="GG").values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).filter(Q(status_id = 58) | Q(status_id = 63)).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']
                    if stat == 55 :
                        f_stat = 1
                    else:
                        f_stat = 0
                        
                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'description':i['description'],
                    'date':f_date,
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'status':f_stat,                    
                    }
                    
                    details.append(val)
                    # increase_variable_after_working_hours.delay(new_data.id)
            return JsonResponse({'data':details},status=200)
        elif role ==48:
            user_hostel = Student.objects.filter(hostel_name ="CG").values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).filter(Q(status_id = 58) | Q(status_id = 63)).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']
                    if stat == 55:
                        f_stat = 1
                    else:
                        f_stat = 0
                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'description':i['description'],
                    'date':f_date,
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'status':f_stat,                    
                    }
                    
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role==49:
            user_hostel = Student.objects.filter(hostel_name ="CV").values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).filter(Q(status_id = 58) | Q(status_id = 63)).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']
                    if stat == 55:
                        f_stat = 1
                    else:
                        f_stat = 0
                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'description':i['description'],
                    'date':f_date,
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'status':f_stat,                    
                    }
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role == 27:
            user_hostel = Student.objects.filter(Q(hostel_name="GG") | Q(hostel_name="SJ")).values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =67).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']
                    if stat == 55:
                        f_stat = 1
                    else:
                        f_stat = 0
                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'description':i['description'],
                    'date':f_date,
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'status':f_stat,                    
                    }
                    
            return JsonResponse({'data':details},status=200)
        elif role ==53:
            user_hostel = Student.objects.filter(Q(hostel_name="CG") | Q(hostel_name="CV")).values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =67).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']
                    if stat == 55:
                        f_stat = 1
                    else:
                        f_stat = 0
                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'description':i['description'],
                    'date':f_date,
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'status':f_stat,                    
                    }
                    
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        
        else:
            return JsonResponse({'error':'You are not allowed to access this page'},status =403)
        
    else:
        return JsonResponse({"error":'Invalid Method'},status = 405)
    

def approve_grievance(request):
    if request.method == "PATCH":
        user =request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
        user_id = user.id
        user_role = UserRole.objects.filter(user_id = user_id).filter(is_active =1).values()
        role = user_role[0]['role_id']
        data = json.loads(request.body)
        grievance_id = data.get('id')
        if role ==25 or role ==43 or role==44 or role ==45:
            user_ = UserRole.objects.filter(user_id =user_id).filter(role_id = role).values()
            id = user_[0]['id']
            status_det = Dropdown.objects.filter(key =4).values()
            status = status_det[0]['id']
            ManageGrievance.objects.create(grievance_id = grievance_id,status_id =status,user_role_id =id)
            GrievanceAdded.objects.filter(id = grievance_id).update(status_id =status)
            return JsonResponse({"message":'Grievance forwarded to Admin officer successfully!'},status =200)
        elif role == 46 or role==47 or role==48 or role==49:
            user_ = UserRole.objects.filter(user_id =user_id).filter(role_id = role).values()
            id = user_[0]['id']
            status_det = Dropdown.objects.filter(key =8).values()
            status = status_det[0]['id']
            ManageGrievance.objects.create(grievance_id = grievance_id,status_id =status,user_role_id =id)
            GrievanceAdded.objects.filter(id = grievance_id).update(status_id =status)
            
            return JsonResponse({"message":'Grievance forwarded to Admin officer successfully!'},status =200)
        elif role==53 or role == 27:
            user_ = UserRole.objects.filter(user_id =user_id).filter(role_id = role).values()
            id = user_[0]['id']
            status_det = Dropdown.objects.filter(key =12).values()
            status = status_det[0]['id']
            ManageGrievance.objects.create(grievance_id = grievance_id,status_id =status,user_role_id =id)
            GrievanceAdded.objects.filter(id = grievance_id).update(status_id =status)
            ManageGrievance.objects.create(grievance_id = grievance_id,status_id =71,user_role_id =id)
            GrievanceAdded.objects.filter(id = grievance_id).update(status_id =71)
            return JsonResponse({"message":'Grievance forwarded to Admin officer successfully!'},status =200)
        elif role ==28:
            user_ = UserRole.objects.filter(user_id =user_id).filter(role_id = role).values()
            id = user_[0]['id']
            status_det = Dropdown.objects.filter(key =16).values()
            status = status_det[0]['id']
            ManageGrievance.objects.create(grievance_id = grievance_id,status_id =status,user_role_id =id)
            GrievanceAdded.objects.filter(id = grievance_id).update(status_id =status)
            ManageGrievance.objects.create(grievance_id = grievance_id,status_id =72,user_role_id =id)
            GrievanceAdded.objects.filter(id = grievance_id).update(status_id =72)
            return JsonResponse({"message":'Grievance forwarded to Admin officer successfully!'},status =200)
        elif role ==24:
            status_det = Dropdown.objects.filter(key =2).values()
            status = status_det[0]['id']
            user_ = UserRole.objects.filter(user_id =user_id).filter(role_id = role).values()
            id = user_[0]['id']
            ManageGrievance.objects.create(grievance_id = grievance_id,status_id =status,user_role_id =id)
            GrievanceAdded.objects.filter(id = grievance_id).update(status_id =status)
            return JsonResponse({"message":'Grievance closed successfully'},status=200)


    else:
        return JsonResponse({"error":'Invalid Method'},status =405)
    
    
    
def reject_grievance(request):
    if request.method == "PATCH":
        user =request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
        user_id = user.id
        user_role = UserRole.objects.filter(user_id = user_id).filter(is_active =1).values()
        role = user_role[0]['role_id']
        if role ==25 or role ==43 or role==44 or role ==45:
            data = json.loads(request.body)
            grievance_id = data.get('id')
            if grievance_id is None:
                return JsonResponse({'error':'Please enter valid grievance id'},status =400)
            reason = data.get('message')
            if reason is not None:
                if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,50}$",reason)):
                    return JsonResponse({'error':'Please enter a valid reason'},status =400)
            else:
                return JsonResponse({'error':'Please enter a valid reason'},status =400)
            user_ = UserRole.objects.filter(user_id =user_id).filter(role_id = role).values()
            id = user_[0]['id']
            status_det = Dropdown.objects.filter(key = 1).values()
            status = status_det[0]['id']
            ManageGrievance.objects.create(grievance_id = grievance_id,reason =reason,status_id =status,user_role_id =id)
            GrievanceAdded.objects.filter(id= grievance_id).update(status_id = status)
            return JsonResponse({"message":'Grievance resolved successfully!'},status =200)
        elif role ==24:
            data = json.loads(request.body)
            grievance_id = data.get('id')
            reason = data.get('message')
            if grievance_id is None:
                return JsonResponse({'error':'Please enter valid grievance id'},status =400)
            reason = data.get('message')
            if reason is not None:
                if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,50}$",reason)):
                    return JsonResponse({'error':'Please enter a valid reason'},status =400)
            else:
                return JsonResponse({'error':'Please enter a valid reason'},status =400)
            status_det = Dropdown.objects.filter(key =3).values()
            status = status_det[0]['id']
            user_ = UserRole.objects.filter(user_id =user_id).filter(role_id = role).values()
            id = user_[0]['id']
            ManageGrievance.objects.create(grievance_id = grievance_id,status_id =status,user_role_id =id,reason = reason)
            GrievanceAdded.objects.filter(id = grievance_id).update(status_id =status)
            return JsonResponse({'message':'Grievance forwarded successfully'},status=200)
    else:
        return JsonResponse({"error":'Invalid Method'},status =405)


def grievance_history(request):
    if request.method == "GET":
        user =request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
        user_id = user.id
        user_role = UserRole.objects.filter(user_id = user_id).filter(is_active =1).values()
        role = user_role[0]['role_id']
        details =[]
        
        if role == 24:            
            if not GrievanceAdded.objects.filter(user_id = user_id).filter(Q(status_id =57)|Q(status_id =62)|Q(status_id =66)|Q(status_id =70)|Q(status_id =74)).exists():
                return JsonResponse({'data':details},status =200)
            user_grievance = GrievanceAdded.objects.filter(user_id = user_id).filter(Q(status_id =57)|Q(status_id =62)|Q(status_id =66)|Q(status_id =70)|Q(status_id =74)).values()
            print(user_grievance)
            for item in user_grievance:
                date = item['date']
                f_date = formatdate(date)
                id  =item['id']

                manage = ManageGrievance.objects.filter(grievance_id =id).order_by('id').values()
                for i in manage:
                    det = ManageGrievance.objects.filter(grievance_id =id).filter(Q(status_id =57)|Q(status_id =62)|Q(status_id =66)|Q(status_id =70)|Q(status_id =74)).values()
                    date = det[0]['date']
                    c_date = formatdate(date)
                val = {
                    'id':id,
                    'title': item['title'],
                    'description':item['description'],
                    'date':f_date,
                    'image':item['images'],
                    'message':i['reason'],
                    'closed_date':c_date
                }
                details.append(val)
            return JsonResponse({'data':details},status =200)
    else:
        return JsonResponse({"error":'Invalid Method'},status = 405)
    
    
def all_grievance(request):
    if request.method == "GET":
        user =request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
        user_id = user.id
        user_role = UserRole.objects.filter(user_id = user_id).filter(is_active =1).values()
        role = user_role[0]['role_id']
        details =[]
        if role ==47 or role == 25:
            user_hostel = Student.objects.filter(hostel_name ="SJ").values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                hostel = items['hostel_name']
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']

                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'date':f_date,
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'hostel_name':hostel,
                    }
                    if stat ==58:
                        message = "Closed"
                    else:
                        message = "Pending"
                    val['message']  = message
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role ==43 or role == 46:
            user_hostel = Student.objects.filter(hostel_name ="GG").values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                hostel = items['hostel_name']
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']

                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'date':f_date,
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'hostel_name':hostel,
                    }
                    if stat ==58:
                        message = "Closed"
                    else:
                        message = "Pending"
                    val['message']  = message
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role ==44 or role == 48:
            user_hostel = Student.objects.filter(hostel_name ="CG").values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                hostel = items['hostel_name']
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']

                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'date':f_date,
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    'hostel_name':hostel,
                    }
                    if stat ==58:
                        message = "Closed"
                    else:
                        message = "Pending"
                    val['message']  = message
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role ==45 or role == 49:
            user_hostel = Student.objects.filter(hostel_name ="CV").values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                hostel = items['hostel_name']

                st_gr = GrievanceAdded.objects.filter(user_id = st_id).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']

                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'date':f_date,
                    'room_number':st_room,
                    'hostel_name':hostel,
                    'name':f_name+" "+l_name,
                    }
                    if stat ==58:
                        message = "Closed"
                    else:
                        message = "Pending"
                    val['message']  = message
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role ==27:
            user_hostel = Student.objects.filter(Q(hostel_name="GG") | Q(hostel_name="SJ")).values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                hostel = items['hostel_name']
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']

                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'date':f_date,
                    'room_number':st_room,
                    'hostel_name':hostel,
                    'name':f_name+" "+l_name,
                    }
                    if stat ==58:
                        message = "Closed"
                    else:
                        message = "Pending"
                    val['message']  = message
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role ==53:
            user_hostel = Student.objects.filter(Q(hostel_name="CG") | Q(hostel_name="CV")).values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                hostel = items['hostel_name']
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']

                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'date':f_date,
                    'room_number':st_room,
                    'hostel_name':hostel,
                    'name':f_name+" "+l_name,
                    }
                    if stat ==58:
                        message = "Closed"
                    else:
                        message = "Pending"
                    val['message']  = message
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role ==29 or role ==23 or role ==28:
            user_hostel = Student.objects.all().values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                hostel = items['hostel_name']
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).order_by('status_id').values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    id = i['id']
                    det = ManageGrievance.objects.filter(grievance_id = id).order_by('-id').values().first()
                    stat = det['status_id']

                    date = i['date']
                    f_date = formatdate(date)
                    val = {
                    'id':i['id'],
                    'title': i['title'],
                    'date':f_date,
                    'room_number':st_room,
                    'hostel_name':hostel,
                    'name':f_name+" "+l_name,
                    }
                    if stat ==58:
                        message = "Closed"
                    else:
                        message = "Pending"
                    val['message']  = message
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role ==24:
            return JsonResponse({'message':details},status =200)
        else:
            return JsonResponse({'error':'You are not allowed to access this page!'},status=403)
        
    else:
        return JsonResponse({'error':'Invalid Method'},status= 405)
    
    
def stats(request):
    if request.method == "GET":
        user =request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
        user_id = user.id
        user_role = UserRole.objects.filter(user_id = user_id).filter(is_active =1).values()
        role = user_role[0]['role_id']
        print(role)
        details =[]
        chart_det=[]
        key=[]
        values=[]
        if role ==25 or role ==47:
            count_total=0
            count_pending =0
            count_closed=0
            count_registered =0
            user_hostel = Student.objects.filter(hostel_name ="SJ").values()
            for items in user_hostel:
                st_id =items['user_id']
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).count()
                count_total = count_total+st_gr
                pending_grievance = GrievanceAdded.objects.filter(user_id = st_id).exclude(status_id =58).count()
                count_pending = count_pending + pending_grievance
                closed_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =58).count()
                count_closed = count_closed+closed_grievance
                reg_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =55).count()
                count_registered = reg_grievance+count_registered
                # category wise
                st_gri = GrievanceAdded.objects.filter(user_id = st_id).values('category_id').distinct()
                for items in st_gri:
                    id = items['category_id']
                    st_gri = GrievanceAdded.objects.filter(user_id = st_id).filter(category_id =id).count()
                    det= Dropdown.objects.filter(id=id).values()
                    value = det[0]['value']
                    key.append(value)
                    values.append(st_gri)
                #chart-date
                st_gri = GrievanceAdded.objects.filter(user_id = st_id).values('date').distinct()
                print(st_gri)
                    
                val={
                    'total':count_total,
                    'pending':count_pending,
                    'closed':count_closed,
                    'registered':count_registered
                }
            chart_det.append(key)
            chart_det.append(values)
            details.append(val)
            return JsonResponse({"data":details,"donut":chart_det},status=200)
        if role ==43 or role ==46:
            count_total=0
            count_pending =0
            count_closed=0
            count_registered =0
            user_hostel = Student.objects.filter(hostel_name ="GG").values()
            for items in user_hostel:
                st_id =items['user_id']
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).count()
                count_total = count_total+st_gr
                pending_grievance = GrievanceAdded.objects.filter(user_id = st_id).exclude(status_id =58).count()
                count_pending = count_pending + pending_grievance
                closed_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =58).count()
                count_closed = count_closed+closed_grievance
                reg_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =55).count()
                count_registered = reg_grievance+count_registered
                st_gri = GrievanceAdded.objects.filter(user_id = st_id).values('category_id').distinct()
                for items in st_gri:
                    id = items['category_id']
                    st_gri = GrievanceAdded.objects.filter(user_id = st_id).filter(category_id =id).count()
                    det= Dropdown.objects.filter(id=id).values()
                    value = det[0]['value']
                    key.append(value)
                    values.append(st_gri)
                
                    
                val={
                    'total':count_total,
                    'pending':count_pending,
                    'closed':count_closed,
                    'registered':count_registered
                }
            chart_det.append(key)
            chart_det.append(values)
            details.append(val)
            return JsonResponse({"data":details,"donut":chart_det},status=200)
        if role ==44 or role ==48:
            count_total=0
            count_pending =0
            count_closed=0
            count_registered =0
            user_hostel = Student.objects.filter(hostel_name ="CG").values()
            for items in user_hostel:
                st_id =items['user_id']
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).count()
                count_total = count_total+st_gr
                pending_grievance = GrievanceAdded.objects.filter(user_id = st_id).exclude(status_id =58).count()
                count_pending = count_pending + pending_grievance
                closed_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =58).count()
                count_closed = count_closed+closed_grievance
                reg_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =55).count()
                count_registered = reg_grievance+count_registered
                st_gri = GrievanceAdded.objects.filter(user_id = st_id).values('category_id').distinct()
                for items in st_gri:
                    id = items['category_id']
                    st_gri = GrievanceAdded.objects.filter(user_id = st_id).filter(category_id =id).count()
                    det= Dropdown.objects.filter(id=id).values()
                    value = det[0]['value']
                    key.append(value)
                    values.append(st_gri)
                
                    
                val={
                    'total':count_total,
                    'pending':count_pending,
                    'closed':count_closed,
                    'registered':count_registered
                }
            chart_det.append(key)
            chart_det.append(values)
            details.append(val)
            return JsonResponse({"data":details,"donut":chart_det},status=200)
        if role == 45 or role ==49:
            count_total=0
            count_pending =0
            count_closed=0
            count_registered =0
            user_hostel = Student.objects.filter(hostel_name ="CV").values()
            for items in user_hostel:
                st_id =items['user_id']
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).count()
                count_total = count_total+st_gr
                pending_grievance = GrievanceAdded.objects.filter(user_id = st_id).exclude(status_id =58).count()
                count_pending = count_pending + pending_grievance
                closed_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =58).count()
                count_closed = count_closed+closed_grievance
                reg_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =55).count()
                count_registered = reg_grievance+count_registered
                st_gri = GrievanceAdded.objects.filter(user_id = st_id).values('category_id').distinct()
                for items in st_gri:
                    id = items['category_id']
                    st_gri = GrievanceAdded.objects.filter(user_id = st_id).filter(category_id =id).count()
                    det= Dropdown.objects.filter(id=id).values()
                    value = det[0]['value']
                    key.append(value)
                    values.append(st_gri)
                
                    
                val={
                    'total':count_total,
                    'pending':count_pending,
                    'closed':count_closed,
                    'registered':count_registered
                }
            chart_det.append(key)
            chart_det.append(values)
            details.append(val)
            return JsonResponse({"data":details,"donut":chart_det},status=200)
        if role ==24:
            count_total=0
            count_pending =0
            count_closed=0
            count_registered =0
            st_gr = GrievanceAdded.objects.filter(user_id = user_id).count()
            count_total = count_total+st_gr
            pending_grievance = GrievanceAdded.objects.filter(user_id = user_id).exclude(status_id =58).count()
            count_pending = count_pending + pending_grievance
            closed_grievance = GrievanceAdded.objects.filter(user_id = user_id).filter(status_id =58).count()
            count_closed = count_closed+closed_grievance
            reg_grievance = GrievanceAdded.objects.filter(user_id = user_id).filter(status_id =55).count()
            count_registered = reg_grievance+count_registered
            st_gri = GrievanceAdded.objects.filter(user_id = user_id).values('category_id').distinct()
            for items in st_gri:
                    id = items['category_id']
                    st_gri = GrievanceAdded.objects.filter(user_id = user_id).filter(category_id =id).count()
                    det= Dropdown.objects.filter(id=id).values()
                    value = det[0]['value']
                    key.append(value)
                    values.append(st_gri)
                
                    
            val={
                    'total':count_total,
                    'pending':count_pending,
                    'closed':count_closed,
                    'registered':count_registered
                }
            chart_det.append(key)
            chart_det.append(values)
            details.append(val)
            return JsonResponse({"data":details,"donut":chart_det},status=200)
        if role==27:
            count_total=0
            count_pending =0
            count_closed=0
            count_registered =0
            user_hostel = Student.objects.filter(Q(hostel_name="GG") | Q(hostel_name="SJ")).values()
            for items in user_hostel:
                st_id =items['user_id']
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).count()
                count_total = count_total+st_gr
                pending_grievance = GrievanceAdded.objects.filter(user_id = st_id).exclude(status_id =58).count()
                count_pending = count_pending + pending_grievance
                closed_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =58).count()
                count_closed = count_closed+closed_grievance
                reg_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =55).count()
                count_registered = reg_grievance+count_registered
                st_gri = GrievanceAdded.objects.filter(user_id = st_id).values('category_id').distinct()
                for items in st_gri:
                    id = items['category_id']
                    st_gri = GrievanceAdded.objects.filter(user_id = st_id).filter(category_id =id).count()
                    det= Dropdown.objects.filter(id=id).values()
                    value = det[0]['value']
                    key.append(value)
                    values.append(st_gri)
                
                    
                val={
                    'total':count_total,
                    'pending':count_pending,
                    'closed':count_closed,
                    'registered':count_registered
                }
            chart_det.append(key)
            chart_det.append(values)
            details.append(val)
            return JsonResponse({"data":details,"donut":chart_det},status=200)
        elif role ==53:
            count_total=0
            count_pending =0
            count_closed=0
            count_registered =0
            user_hostel = Student.objects.filter(Q(hostel_name="CG") | Q(hostel_name="CV")).values()
            for items in user_hostel:
                st_id =items['user_id']
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).count()
                count_total = count_total+st_gr
                pending_grievance = GrievanceAdded.objects.filter(user_id = st_id).exclude(status_id =58).count()
                count_pending = count_pending + pending_grievance
                closed_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =58).count()
                count_closed = count_closed+closed_grievance
                reg_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =55).count()
                count_registered = reg_grievance+count_registered
                st_gri = GrievanceAdded.objects.filter(user_id = st_id).values('category_id').distinct()
                for items in st_gri:
                    id = items['category_id']
                    st_gri = GrievanceAdded.objects.filter(user_id = st_id).filter(category_id =id).count()
                    det= Dropdown.objects.filter(id=id).values()
                    value = det[0]['value']
                    key.append(value)
                    values.append(st_gri)
                
                    
                val={
                    'total':count_total,
                    'pending':count_pending,
                    'closed':count_closed,
                    'registered':count_registered
                }
            chart_det.append(key)
            chart_det.append(values)
            details.append(val)
            return JsonResponse({"data":details,"donut":chart_det},status=200)
        elif role ==23 or role ==29 or role==28:
            count_total=0
            count_pending =0
            count_closed=0
            count_registered =0
            user_hostel = Student.objects.all().values()
            for items in user_hostel:
                st_id =items['user_id']
                st_gr = GrievanceAdded.objects.filter(user_id = st_id).count()
                count_total = count_total+st_gr
                pending_grievance = GrievanceAdded.objects.filter(user_id = st_id).exclude(status_id =58).count()
                count_pending = count_pending + pending_grievance
                closed_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =58).count()
                count_closed = count_closed+closed_grievance
                reg_grievance = GrievanceAdded.objects.filter(user_id = st_id).filter(status_id =55).count()
                count_registered = reg_grievance+count_registered
                st_gri = GrievanceAdded.objects.filter(user_id = st_id).values('category_id').distinct()
                for items in st_gri:
                    id = items['category_id']
                    st_gri = GrievanceAdded.objects.filter(user_id = st_id).filter(category_id =id).count()
                    det= Dropdown.objects.filter(id=id).values()
                    value = det[0]['value']
                    key.append(value)
                    values.append(st_gri)
                
                    
                val={
                    'total':count_total,
                    'pending':count_pending,
                    'closed':count_closed,
                    'registered':count_registered
                }
            chart_det.append(key)
            chart_det.append(values)
            details.append(val)
            return JsonResponse({"data":details,"donut":chart_det},status=200)
    else:
        return JsonResponse({"error":"Invalid Method"},status = 405)