from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from bankapp.models import application, Branch, District
from .forms import ApplicationForm
import json

app_name='bankapp'


# Create your views here.

def index(request):
    return render(request,"index.html")

# def index(request,):
#     bank=application.objects.all()
#     context={'application_list':bank}
#     return render(request,"index.html",context)
#



def register(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken")
                return redirect('/register')
            else:
                user =User.objects.create_user(username=username, password=password)
                user.save();
                return redirect('/login')

                # print("User Account Created")
                # return redirect('login')
        else:
            messages.info(request, "Password is Incorrect")
            return redirect('/register')
        return redirect('/')
    return render(request, "register.html")

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/userhome')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('/login')
    return render(request,"login.html")


def userhome(request):
    return render(request,"userhome.html")

# def userhome(request,id):
#     bank=application.objects.get(id=id)
#     context = {'application_list': bank}
#     return render(request,"application.html",context)

# def application_form(request):
#
#         # return redirect('/application_form')
#
#         if request.method == 'POST':
#             name = request.POST['name']
#             dob = request.POST['dob']
#             age = request.POST['age']
#             gender = request.POST['gender']
#             phone = request.POST['phone']
#             email = request.POST['email']
#             address = request.POST['address']
#             district = request.POST['district']
#             branch = request.POST['branch']
#             accounttype = request.POST['accounttype']
#             app = application(name=name, dob=dob, age=age, gender=gender, phone=phone, email=email, address=address, district=district, branch=branch, accounttype=accounttype)
#             app.save()
#             return redirect('/application_form')

        # d = {'district': district}

        # return redirect('/form_save')
        # return render(request,'application.html',{'districts': districts})
def application_form(request):
    if request.method == 'POST':

        name = request.POST['name']
        #request.session['user_id']=
        dob = request.POST['dob']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        # district = request.POST['district']
        # branch = request.POST['branch']
        accounttype = request.POST['accounttype']
        app = application(name=name, dob=dob, age=age, gender=gender, phone=phone, email=email, address=address, accounttype=accounttype)
        app.save();
        messages.info(request, "Application Accepted")
        return redirect('/application_form')
        # return redirect(reverse('/application_view/',kwargs={"application_id": app.pk}))
    districts = District.objects.all()
    return render(request, 'application.html', {'districts': districts})

def application_view(request):
    #id = request.session['user_id']
    current_user = request.user
    id = current_user.id
    print(id)
    bank=application.objects.get(id=id)
    if bank:
       return render(request, 'applicationview.html',{'bank': bank})
    else:
       return render(request, "application.html")


def load_branch(request):
    district_id = request.GET.get('district')
    branch = Branch.objects.filter(district_id=district_id).order_by('name')
    return render(request,'branch_dropdown.html', {'branch':branch})

def logout(request):
    auth.logout(request)
    return redirect('/')

def message(request):
    return render(request,'message.html')