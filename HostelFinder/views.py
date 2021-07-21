from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse
from .models import UserProfile
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render,redirect 
from owner.models import Hostel
from django.db.models import Q
def hostel(request):
    return render(request, "hostel.html")

def signup(request):
    if request.method == "POST":
        fn = request.POST['fname']
        ln = request.POST['lname']
        un = request.POST['uname']
        pwd = request.POST['pwd']
        em = request.POST['email']
        mob = request.POST['mob']
        addr = request.POST['address']
        type = request.POST['type']
        uobj = User(first_name=fn,last_name=ln,username=un,password=make_password(pwd),email=em)
        uobj.save()
        uobj_pro_obj = UserProfile(user=uobj,usertype=type,mobile=mob,address=addr)
        uobj_pro_obj.save()
        return redirect('/signup/')
    return render(request,"signup.html")

def login_call(request):
    if request.method == "POST":
        un = request.POST['uname']
        pwd = request.POST['pwd']
        user = authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            profileobj = UserProfile.objects.get(user__username=request.user)
            if profileobj.usertype == "owner":
                return redirect('/owner/home/')
            elif profileobj.usertype == "student":
                return redirect('/student/home/')
        else:
            return HttpResponse("<h1>Invalid Credential</h1>")
    
            
    return render(request,"login.html")

def logout_call(request):
    logout(request)
    return redirect('/login/')

def search_call(request):
    if 'q' in request.GET:
        q= request.GET['q']
        ser=(Q(name__icontains=q) | Q(price__icontains=q))
        allhostels = Hostel.objects.filter(ser)

    return render(request, 'search.html',{'allhostels':allhostels})

