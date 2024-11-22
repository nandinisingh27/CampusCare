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
from django.contrib.auth.models import User

def faculty_register(request):
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
        return JsonResponse({'message':'Faculty account created successfully'},status = 200)
    else:
        return JsonResponse({'message':"Method not allowed"},status =405)
    
def student_register(request):
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
        phone_number =request.POST['phone_no']
        if phone_number is not None:
            if not bool(re.match(r"^[6-9]{1}[0-9]{9}$",phone_number)):
                return JsonResponse({'error':'Please enter a valid phone number'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid phone number'},status =400)
        image = request.FILES['profile_image']
        branch = request.POST['department']
        print(branch)
        if branch is  None:
            return JsonResponse({'error':'Please enter a valid branch'},status =400)

        address = request.POST['address']
        if address is None:
            return JsonResponse({'error':'Please enter a valid address'},status =400)
        hostel_name = request.POST['hostel']
        if hostel_name is not None:
            if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,20}$",hostel_name)):
                return JsonResponse({'error':'Please enter a valid hostel name'},status =400)
        else:
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
        if gender is not None:
            if not bool(re.match(r"^[A-Za-z]{1}$",gender)):
                return JsonResponse({'error':'Please enter valid gender'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid gender'},status =400)
        user = User.objects.create_user(first_name= first_name,username=email,last_name=last_name,password = password)
        Student.objects.create(image= image,user=user,hostel_name=hostel_name,room_number=room_number,address = address,gender=gender,Department =branch)
        return JsonResponse({'message':'Student account created successfully'},status = 200)
    else:
        return JsonResponse({'message':"Method not allowed"},status =405)

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
    role_info = User_role.objects.filter(user_id =  user_id).values_list()
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
        print(role_)
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
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            role = role_type(user)
            role_key = role_type_key(user)
            print(role_key)
            user_info = User.objects.filter(username = user).values()
            is_staff = user_info[0]['is_staff']
            if is_staff:
                nav = Navbar.objects.filter(role ="FT").filter(position = 1).values()
                state = nav[0]['link']
                return JsonResponse({'message': "Successfully logged in!",'state':state,'role':role},status =200)
            else:
                nav = Navbar.objects.filter(role = "S").filter(position = 1).values()
                state = nav[0]['link']
                return JsonResponse({'message':"Successfully logged in!",'state':state,'role':role},status =200)
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
        type = request.GET.get('type')
        
        info = Drop_down.objects.filter(value =type).values()
        type_id = info[0]['id']
        det = Drop_down.objects.filter(parent_id = type_id).values()
        details=[]
        for item in det:
            val={
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
        user_det = User.objects.filter(username =user).values()
        is_staff = user_det[0]['is_staff']
        print(is_staff)
        _id = user_det[0]['id']
        role = role_type(user)
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
                    values={
                'name':name,
                'email':email,
                'image':item['image'],
                'hostel':item['hostel_name'],
                'room_no':item['room_number'],
                'role':role,
                'department':item['Department'],
                'gender':gender,
                'address':item['address']
                    }
                userDet.append(values)
        return JsonResponse({'data':userDet},status =200)
    else:
        return JsonResponse({'error':'Method not allowed'},status =405)
    
def list_faculty(request):
    if request.method == "GET":
        user = request.user
        role = role_type(user)
        print(role)
        if role == "Dean SW":
            details =[]
            fac= Faculty.objects.all().exclude(role="DSW").exclude(role="AD").values()
            for item in fac:
                id = item['user_id']
                
                user_det = User.objects.filter(id =id).values()
                f_name= user_det[0]['first_name']
                l_name = user_det[0]['last_name']
                name =f_name+" "+l_name
                email = user_det[0]['username']
                role = role_type(email)
                val = {
                    'name':name,
                    'email':email,
                    'image':item['image'],
                    'experience':item['experience'],
                    'qualification':item['qualification'],
                    'role':role
                }
                details.append(val)
                            
            return JsonResponse({"list":details},status =200)
    elif request.method == "PUT":
        pass
    else:
        return JsonResponse({'error':'Method not allowed'},status =405)
    
    
def list_roles(request):
    pass   

def navbar(request):
    if request.method == "GET":
        user = request.user
        role = role_type_key(user)
        child = Navbar.objects.filter(role =role).filter(is_parent =1).values()
        

        items = Navbar.objects.filter(role =role).filter(is_parent =0).values()
        
    