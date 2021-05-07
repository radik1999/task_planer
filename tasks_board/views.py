import json

from django.conf.urls import url
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Goal, DailyTask
from .business import save_task_form


@login_required
def all_tasks(request):
    tasks = DailyTask.objects.all()
    goals = Goal.objects.all()

    return render(request, 'tasks_board/all_tasks.html', {'tasks': tasks, 'goals': goals})


@login_required
def add_task(request):
    if request.method == 'POST':
        result = save_task_form(request)
        return HttpResponse(result)


@login_required
def current_day(request):
    return render(request, 'tasks_board/today.html')


@login_required
def upcoming(request):
    return render(request, 'tasks_board/upcoming.html')


def sign_out(request):
    logout(request)
    return redirect('board:today')


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('board:today')
    else:
        form = UserCreationForm()
    return render(request, 'tasks_board/signup.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return HttpResponse(json.dumps({'message': "Success"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'message': "Denied"}), content_type='application/json')



