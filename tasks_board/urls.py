from django.urls import path


from tasks_board.views import (
    all_tasks, sign_up, sign_in, sign_out, current_day, upcoming,
    add_task, task, change_status, edit_task, delete_task, completed_tasks,
    goal, add_goal, all_goals, edit_goal, delete_goal
)


app_name = 'board'

urlpatterns = [
    path('signout', sign_out, name='sign_out'),
    path('signin/', sign_in, name='sign_in'),
    path('signup/', sign_up, name='sign_up'),
    path('', current_day, name='today'),
    path('tasks/', all_tasks, name='tasks'),
    path('add_task/', add_task, name='add_task'),
    path('upcoming/', upcoming, name='upcoming'),
    path('task/<int:task_id>', task, name='task'),
    path('change_status/<int:task_id>', change_status, name='change_status'),
    path('edit_task/<int:task_id>', edit_task, name='edit_task'),
    path('delete_task/<int:task_id>', delete_task, name='delete_task'),
    path('completed_tasks/', completed_tasks, name='completed_tasks'),
    path('goals', all_goals, name='goals'),
    path('goal/<int:goal_id>', goal, name='goal'),
    path('add_goal/', add_goal, name='add_goal'),
    path('edit_goal/<int:goal_id>', edit_goal, name='edit_goal'),
    path('delete_goal/<int:goal_id>', delete_goal, name='delete_goal'),

]
