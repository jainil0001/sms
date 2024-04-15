from django.shortcuts import render, redirect, HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import CustomUser

def BASE(request):
    return render(request,'base.html')


def LOGIN(request):
    return render(request,'login.html')


def dbLogin(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password = request.POST.get('password'),)
        if user is not None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('hod_home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return redirect('student_home')
            else:
                messages.error(request,'Email and Password are Invalid')
                return redirect('login')
        else:
            messages.error(request, 'Email and Password are Invalid')
            return redirect('login')


def dologout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/')
def profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        'user':user,
    }
    return render(request,'profile.html')

@login_required(login_url='/')
def update_profile(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            customeuser = CustomUser.objects.get(id=request.user.id)
            customeuser.first_name = first_name
            customeuser.last_name = last_name
            customeuser.email = email

            if password is not None and password != '':
                customeuser.set_password(password)
            if profile_pic is not None and profile_pic != '':
                customeuser.profile_pic = profile_pic

            customeuser.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect('profile')
        except:
            messages.error(request,'Profile Update Failed')
            # return redirect('profile')
    return render(request,'profile.html')