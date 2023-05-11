from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Student
from django.db import IntegrityError
from .forms import AddStudentForm

# home view
def index_view(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # throw error when user exists
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            return redirect('student_list')
        except IntegrityError:
            messages.error(request, 'Username Already Exists')
            return redirect('register')
    else:
        return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # login if anthenticate success
        if user is not None:
            login(request, user)
            return redirect('student_list')
        else:
            message = 'Incorrect Username or Password Entered'
            messages.error(request, message)
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def student_list_view(request):
    students = Student.objects.filter(user=request.user)
    context = {'students': students}
    return render(request, 'student_list.html', context)


@login_required(login_url='login')
def add_student_view(request):
    form = AddStudentForm(request.POST)
    if form.is_valid():
        # make the user the current login user
        student = form.save(commit=False)
        student.user = request.user
        student.save()
        return redirect('student_list')
    else:
        form = AddStudentForm()
        context = {'form': form}
        return render(request, 'add_student.html', context)