from django.shortcuts import render
import re
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse
from .models import Faculty
from .models import Student
from .models import Drop_down
from .models import Navbar
from .models import User_role
from .models import Grievance
from .models import Grievance_manage
from django.contrib.auth.models import User

def faculty_register(request):
    user =request.user
    if not user.is_authenticated:
        return JsonResponse({"error":"Unauthorized"},status =401)
    else:
        user_det = User.objects.filter(username =user).values()
        id =user_det[0]['id']
        user_role =User_role.objects.filter(user_id =id).filter(is_active=1).values()
        role_id = user_role[0]['role_id']
        if role_id == 29:        
            if request.method=="POST":
                first_name = request.POST['first_name']
                print(first_name)
                if first_name is not None:
                    if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,29}$",first_name)):
                        return JsonResponse({'error':'Please enter a valid first name'},status =400)
                else:
                        return JsonResponse({'error':'Please enter first name'},status =400)
                        
                last_name = request.POST['last_name']
                email = request.POST['email']
                if User.objects.filter(username = email).exists():
                    return JsonResponse({"error":'Email already exist, Please register with another email'},status =400)
                if email is not None:
                    if not bool(re.match(r"[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}",email)):
                        return JsonResponse({'error':'Please enter a valid email'},status =400)
                else:
                        return JsonResponse({'error':'Please enter a valid email ID'},status =400)
                address = request.POST['address']
                if address is None:
                    return JsonResponse({'error':'Please enter a valid address'},status =400)
                phone_number =request.POST['phone_no']
                if phone_number is not None:
                    if not bool(re.match(r"^[6-9]{1}[0-9]{9}$",phone_number)):
                        return JsonResponse({'error':'Please enter a valid phone number'},status =400)
                else:
                        return JsonResponse({'error':'Please enter a valid phone number'},status =400)
                if len(request.FILES)!= 0:
                    image = request.FILES['profile_image']
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
                if gender is not None:
                    if not bool(re.match(r"^[a-zA-Z]+$",gender)):
                        return JsonResponse({'error':'Please enter valid gender'},status =400)
                else:
                    return JsonResponse({'error':'Please enter valid gender'},status =400)
                qualification = request.POST['qualification']
                if qualification is None:
                    return JsonResponse({'error':'Please a enter valid qualification'},status =400)
                experience=request.POST['experience']
                user = User.objects.create_user(first_name= first_name,username=email,last_name=last_name,password = password, is_staff = 1)
                Faculty.objects.create(user=user,experience=experience,qualification=qualification,gender =gender,image = image,address = address)
                lst = Drop_down.objects.filter(key = "FT").values()
                id = lst[0]['id']
                user_det = User.objects.filter(username = email).values()
                user_ID = user_det[0]['id']
                User_role.objects.create(user_id = user_ID,is_active = 1,role_id = id)
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
        user_det = User.objects.filter(username =user).values()
        id =user_det[0]['id']
        user_role =User_role.objects.filter(user_id =id).filter(is_active=1).values()
        role_id = user_role[0]['role_id']
        if role_id == 29:        
            if request.method=="POST":
                first_name = request.POST['first_name']
                if first_name is not None:
                    if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,29}$",first_name)):
                        return JsonResponse({'error':'Please enter a valid first name'},status =400)
                else:
                    return JsonResponse({'error':'Please enter a valid first name'},status =400)
                last_name = request.POST['last_name']
                email = request.POST['email']
                
                if email is not None:
                    if not bool(re.match(r"[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}",email)):
                        return JsonResponse({'error':'Please enter a valid email'},status =400)
                else:
                    return JsonResponse({'error':'Please enter a valid email ID'},status =400)
                if User.objects.filter(username = email).exists():
                    return JsonResponse({"error":'Email already exist, Please register with another email'},status =400)
                phone_number =request.POST['phone_no']
                if phone_number is not None:
                    if not bool(re.match(r"^[6-9]{1}[0-9]{9}$",phone_number)):
                        return JsonResponse({'error':'Please enter a valid phone number'},status =400)
                else:
                    return JsonResponse({'error':'Please enter a valid phone number'},status =400)
                image = request.FILES['profile_image']
                branch = request.POST['department']
                if branch is  None:
                    return JsonResponse({'error':'Please enter a valid branch'},status =400)

                address = request.POST['address']
                if address is None:
                    return JsonResponse({'error':'Please enter a valid address'},status =400)
                hostel_name = request.POST['hostel']
                if hostel_name is  None:
                    return JsonResponse({'error':'Please enter a valid hostel name'},status =400)
                room_number = request.POST['room_no']
                if room_number  is not None:
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
                if gender is None:

                    return JsonResponse({'error':'Please enter valid gender'},status =400)
                user = User.objects.create_user(first_name= first_name,username=email,last_name=last_name,password = password)
                Student.objects.create(image= image,user=user,hostel_name=hostel_name,room_number=room_number,address = address,gender=gender,Department =branch)
                lst = Drop_down.objects.filter(key = "S").values()
                id = lst[0]['id']
                user_det = User.objects.filter(username = email).values()
                user_ID = user_det[0]['id']
                User_role.objects.create(user_id =user_ID , role_id = id,is_active = 1)
                return JsonResponse({'message':'Student account created successfully'},status = 200)
            else:
                return JsonResponse({'message':"Method not allowed"},status =405)
        else:
            return JsonResponse({"error":'You are not allowed to access this page'},status=403)

def role_type_key(user):
    info = User.objects.filter(username=user).values()
    user_id= info[0]['id']
    role_info = User_role.objects.filter(user_id =  user_id).values_list()
    details =[]
    for i in role_info:
        role_id= i[2]
        role_det = Drop_down.objects.filter(id = role_id).values()
        role = role_det[0]['key']
        val = {
        'role':role,
            'id':role_id
        }
        details.append(val)
    return details


def role_type(user):
    info = User.objects.filter(username=user).values()
    user_role = info[0]['is_staff']
    user_id= info[0]['id']    
    role_info = User_role.objects.filter(user_id =  user_id).filter(is_deleted =0).values_list()
    details =[]
    for i in role_info:
        role_id= i[2]
        role_det = Drop_down.objects.filter(id = role_id).values()
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
        role_val = Drop_down.objects.filter(key = role_).values()
        gender = role_val[0]['value']
        
        return gender
    else:
        role_info = Student.objects.filter(user_id =  user_id).values()
        role_ = role_info[0]['gender']
        role_val = Drop_down.objects.filter(key = role_).values()
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
            role_det = User_role.objects.filter(user_id =user_ID).filter(is_active = 1).values()
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
        det = Drop_down.objects.filter(parent_id = type).values()
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
        is_staff = user_det[0]['is_staff']
        _id = user_det[0]['id']
        user_data= User_role.objects.filter(user_id = _id).filter(is_active=True).values()
        role_id = user_data[0]['role_id']
        data = Drop_down.objects.filter(id = role_id).values()
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
                    hostel_ = Drop_down.objects.filter(key = hostel).values()
                    host = hostel_[0]['value']
                    dept = item['Department']
                    dept_ = Drop_down.objects.filter(key = dept).values()
                    dept_m = dept_[0]['value']
                    gender_ = item['gender']
                    gender_e = Drop_down.objects.filter(key = gender_).values()
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
        user_det = User.objects.filter(username = user).values()
        user_id = user_det[0]['id']
        user_role = User_role.objects.filter(user_id = user_id).filter(is_active=1).values()
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
    user_det = User.objects.filter(username =user).values()
    id= user_det[0]['id']
    roles_det = User_role.objects.filter(user_id = id).filter(is_deleted = 0).values()
    
    roles =[]
    for item in roles_det:
        id = item['role_id']
        active = item['is_active']
        role_ = Drop_down.objects.filter(id =id).values()
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
        user_det = User.objects.filter(username = user).values()
        user_i = user_det[0]['id']
        data =json.loads(request.body)
        role_id = data.get('role')
        user_det = User_role.objects.filter(role_id = role_id).values()
        user_id = user_det[0]['user_id']
        user_=User_role.objects.filter(role_id = role_id)
        user_det = User_role.objects.filter(role_id = role_id).values()
        user_id = user_det[0]['user_id']
        user_=User_role.objects.filter(role_id = role_id).filter(user_id = user_i).update(is_active=1)
        user_1 = User_role.objects.filter(role_id = role_id).filter(user_id = user_i).values()
        print(user_1)
        USeR=User_role.objects.filter(user_id = user_i).values().exclude(role_id = role_id).update(is_active = 0)
        USeR_=User_role.objects.filter(user_id = user_i).exclude(role_id = role_id).values()
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
        user_det = User.objects.filter(username = user).values()
        user_id = user_det[0]['id']
        role_det = User_role.objects.filter(user_id = user_id).filter(is_active = True).values()
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
        user_role = User_role.objects.filter(user_id = user_id).filter(is_active =1).values()
        rol = user_role[0]['role_id']
        if rol == 28:
                data = json.loads(request.body)
                role = data.get('role')
                user_id = data.get('user_id')
                User_role.objects.create(user_id = user_id , role_id =role)
                return JsonResponse({'message':'Role added successfully'},status = 200)
        else:
            return JsonResponse({"error":"You are not allowed to access this page"},status=403)
    elif request.method == "PATCH":
        data  = json.loads(request.body)
        print(data)
        user_d = data.get('user')
        role_id = data.get('role')   
        lst = User_role.objects.filter(user_id = user_d).filter(role_id= role_id).update(is_deleted = 1)
        print(lst)
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
        user_role = User_role.objects.filter(user_id = user_id).filter(is_active =1).values()
        rol = user_role[0]['role_id']
        if rol == 24:
                title = request.POST['title']
                if title is not None:
                    if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,29}$",title)):
                        return JsonResponse({'error':'Please enter a valid title'},status =400)
                else:
                    return JsonResponse({'error':'Please enter a valid title'},status =400)
                description = request.POST['description']
                if description is  None:
                    return JsonResponse({'error':'Please enter a valid description'},status =400)
                if len(request.FILES)!= 0:
                    image = request.FILES['image']
                else:
                    return JsonResponse({'error':'Please upload a valid image '},status =400)
                category = request.POST['category']
                if category  is  None:
                    return JsonResponse({'error':'Please enter a valid category'},status =400)
                

                grievance = Grievance.objects.create(user_id = user_id,category_id = category,title =title,description = description,images = image)
                
                return JsonResponse({'message':'Grievance added successfully!'},status =200)
                    
        else:
                return JsonResponse({"error":'You are not allowed to access this page!'},status =403)
    else:
        return JsonResponse({"error":'Invalid Method'},status = 405)

    
def manage_grievance(request):
    if request.method =="POST":
        user =request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
        else:
            pass
            
    else:
        return JsonResponse({'error':"Invalid Method"},status =405)

def list_grievance(request):
    if request.method == "GET":
        user =request.user
        if not user.is_authenticated:
            return JsonResponse({"error":"Unauthorized"},status =401)
        user_id = user.id
        user_role = User_role.objects.filter(user_id = user_id).filter(is_active =1).values()
        role = user_role[0]['role_id']
        details =[]
        status =[]
        if role == 24:            
            if not Grievance.objects.filter(user_id = user_id).exists():
                return JsonResponse({'data':details},status =200)
            user_grievance = Grievance.objects.filter(user_id = user_id).values()
            status.append("Grievance registered")
            for item in user_grievance:
                val = {
                    'title': item['title'],
                    'description':item['description'],
                    'date':item['date'],
                    'image':item['images'],
                    'status':status
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
                
                st_gr = Grievance.objects.filter(user_id = st_id).values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    val = {
                    'title': i['title'],
                    'description':i['description'],
                    'date':i['date'],
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    
                    }
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
                
                st_gr = Grievance.objects.filter(user_id = st_id).values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    val = {
                    'title': i['title'],
                    'description':i['description'],
                    'date':i['date'],
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    
                    }
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        elif role == 44:
            user_hostel = Student.objects.filter(hostel_name ="CG").values()            
            for items in user_hostel:
                st_id =items['user_id']
                user_d = User.objects.filter(id= st_id).values()
                f_name = user_d[0]['first_name']
                l_name =user_d[0]['last_name']
                st_room = items['room_number']
                
                st_gr = Grievance.objects.filter(user_id = st_id).values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    val = {
                        'id':i['id'],
                    'title': i['title'],
                    'description':i['description'],
                    'date':i['date'],
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    
                    }
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
                
                st_gr = Grievance.objects.filter(user_id = st_id).values()
                if not st_gr.exists():
                    return JsonResponse({"data":details},status =200)
                for i in st_gr:
                    val = {
                    'title': i['title'],
                    'description':i['description'],
                    'date':i['date'],
                    'image':i['images'],
                    'room_number':st_room,
                    'name':f_name+" "+l_name,
                    
                    }
                    details.append(val)
            return JsonResponse({'data':details},status=200)
        else:
            return JsonResponse({'error':'You are not allowed to access this page'},status =403)
        
    else:
        return JsonResponse({"error":'Invalid Method'},status = 405)
    
    
    
    
