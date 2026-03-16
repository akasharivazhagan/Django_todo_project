from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
import uuid


def register_view(request):

    form = RegisterForm()

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Email must be unique
            if User.objects.filter(email=email).exists():

                messages.error(request,"Email already exists")
                return render(request,'accounts/register.html',{'form':form})

            # Generate unique username internally
            unique_username = username + "_" + str(uuid.uuid4())[:5]

            user = User.objects.create_user(
                username=unique_username,   # internal unique username
                email=email,
                password=password,
                first_name=username         # store actual username
            )

            messages.success(request,"Registration Successful! Please Login")

            return render(request,'accounts/register.html',{'form':form})

    return render(request,'accounts/register.html',{'form':form})


def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = None

        user = authenticate(request, username=username, password=password)

        if user is not None:
                
            login(request,user)

            return redirect("dashboard")

        else:

            messages.error(request,"Invalid Email or Password")

    return render(request,"accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')



