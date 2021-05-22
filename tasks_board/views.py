import json

from django.conf.urls import url
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import date

from django.urls import reverse

from .models import Goal, DailyTask
from .business.business import save_task_form, change_task_status, save_goal_form
from .business.satistic import Statistic, GoalCategory


def anonymous_user_home(request):
    return render(request, 'tasks_board/not_auth_home.html')


def all_tasks(request):
    request.session['return_page'] = 'board:tasks'
    tasks = DailyTask.objects.filter(main_task=None, status=False, owner=request.user)
    tasks = sorted(tasks, key=lambda t: (t.day, t.priority), reverse=True)
    goals = Goal.objects.all()

    return render(request, 'tasks_board/tasks.html', {'tasks': tasks, 'goals': goals})


def current_day(request):
    request.session['return_page'] = 'board:today'
    tasks = DailyTask.objects.filter(day=date.today(), main_task=None, status=False, owner=request.user)
    tasks = sorted(tasks, key=lambda t: (t.day, t.priority), reverse=True)
    goals = Goal.objects.all()
    return render(request, 'tasks_board/today.html', {'tasks': tasks, 'goals': goals})


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


def task(request, task_id):
    task = DailyTask.objects.get(pk=task_id)
    goals = Goal.objects.all()
    request.session['previous_url'] = request.META['HTTP_REFERER']
    return render(request, 'tasks_board/task.html', {'task': task, 'goals': goals})


def add_task(request):
    if request.method == 'POST':
        result = save_task_form(request)
        return HttpResponse(result)


def change_status(request, task_id):
    task = DailyTask.objects.get(pk=task_id)
    change_task_status(task)
    return HttpResponse('ok')


def edit_task(request, task_id):
    task = DailyTask.objects.get(pk=task_id)
    if request.method == 'POST':
        result = save_task_form(request, task)
        return HttpResponse(result)


def delete_task(request, task_id):
    t = DailyTask.objects.get(pk=task_id)
    main_task = t.main_task
    t.delete()
    if main_task:
        return redirect('board:task', task_id=main_task.id)
    elif request.session['return_page']:
        return redirect(request.session['return_page'])
    return redirect('board:tasks')


def completed_tasks(request):
    request.session['return_page'] = 'board:completed_tasks'
    tasks = DailyTask.objects.filter(status=True, main_task=None, owner=request.user)
    tasks = sorted(tasks, key=lambda t: (t.day, t.priority), reverse=True)
    goals = Goal.objects.all()
    return render(request, 'tasks_board/completed_tasks.html', {'tasks': tasks, 'goals': goals})


def goal(request, goal_id):
    if request.method == 'GET':
        request.session['return_page'] = reverse('board:goal', kwargs={'goal_id': goal_id})
        goal = Goal.objects.get(pk=goal_id)
        goals = Goal.objects.all()
        return render(request, 'tasks_board/goal.html', {'goal': goal, 'goals': goals})


def all_goals(request):
    if request.method == 'GET':
        request.session['return_page'] = 'board:goals'
        goals = Goal.objects.filter(owner=request.user)
        goals = sorted(goals, key=lambda g: g.priority, reverse=True)
        return render(request, 'tasks_board/goals.html', {'goals': goals})


def add_goal(request):
    if request.method == 'POST':
        result = save_goal_form(request)
        return HttpResponse(result)


def delete_goal(request, goal_id):
    Goal.objects.get(pk=goal_id).delete()
    return redirect('board:goals')


def edit_goal(request, goal_id):
    goal = Goal.objects.get(pk=goal_id)
    if request.method == 'POST':
        result = save_goal_form(request, goal)
        return HttpResponse(result)


def back(request):
    return redirect(request.session['return_page'])


def profile(request):
    return render(request, 'tasks_board/profile.html', {'statistic': Statistic(request)})


def chart(request, chart_name):
    if chart_name == 'todaytasks':
        return HttpResponse(Statistic(request).today_tasks.modal_html)
    elif chart_name == 'alltasks':
        return HttpResponse(Statistic(request).all_tasks.modal_html)
    else:
        return HttpResponse(GoalCategory(chart_name).modal_html)
