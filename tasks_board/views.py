import json

from django.conf.urls import url
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import date


from .models import Goal, DailyTask
from .business import save_task_form, change_task_status


def all_tasks(request):
    tasks = DailyTask.objects.filter(main_task=None)
    tasks = sorted(tasks, key=lambda t: (t.priority, t.day), reverse=True)
    goals = Goal.objects.all()

    return render(request, 'tasks_board/tasks.html', {'tasks': tasks, 'goals': goals})


def current_day(request):
    tasks = DailyTask.objects.filter(day=date.today(), main_task=None)
    tasks = sorted(tasks, key=lambda task: (task.priority, task.day), reverse=True)
    goals = Goal.objects.all()
    return render(request, 'tasks_board/today.html', {'tasks': tasks, 'goals': goals})


def upcoming(request):
    return render(request, 'tasks_board/upcoming.html')


def task(request, _id):
    task = DailyTask.objects.get(pk=_id)
    return render(request, 'tasks_board/task.html', {'task': task})


def add_task(request):
    if request.method == 'POST':
        result = save_task_form(request)
        return HttpResponse(result)


def change_status(request, task_id):
    task = DailyTask.objects.get(pk=task_id)
    change_task_status(task)
    return HttpResponse('ok')


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



