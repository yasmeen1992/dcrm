import re
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):
  records = Record.objects.all()
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, 'Login Successful')
      return redirect('home')
    else:
      messages.success(request, "There was an error Logging in ")
      return redirect('home')
  else:
    return render(request, 'home.html', {'records': records})


# def login_user(request):
#   pass


def logout_user(request):
  logout(request)
  messages.success(request, "You have been logged out")
  return redirect('home')


def register_user(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password1')
      user = authenticate(request, username=username, password=password)
      login(request, user)
      messages.success(request, "You Have Succesfully Registered")
      return redirect('home')
  else:
    form = SignUpForm()
    return render(request, 'register.html', {'form': form})
  return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
  if request.user.is_authenticated:
    customer_record = Record.objects.get(id=pk)
    return render(request, 'record.html', {'customer_record': customer_record})
  else:
    messages.success(request, "You must be logged in to view Page")
    return redirect('home')


def delete_record(request, pk):
  if request.user.is_authenticated:
    delete_it = Record.objects.get(id=pk)
    delete_it.delete()
    messages.success(request, "Record Deleted Succesfully")
    return redirect('home')
  else:
    messages.success(request, "You must be logged in to Do that ")
    return redirect('home')


def add_record(request):
  if request.user.is_authenticated:
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
      if request.method == 'POST':
        if form.is_valid():
          form.save()
          messages.success(request, "Record Added Succesfully")
          return redirect('home')
      else:
        return render(request, 'add_record.html', {'form': form})
    else:
      messages.success(request, "You must be logged in to Do that ")
      return redirect('home')
def update_record(request, pk):
  if request.user.is_authenticated:
    current_record = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None,instance=current_record)
    if form.is_valid():
       form.save()
       messages.success(request, "Record Updated Succesfully")
       return redirect('home')
    return render(request, 'update_record.html', {'form': form})
  else:
    messages.success(request, "You must be logged in to Do that ")
    return redirect('home')