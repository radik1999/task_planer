from django.urls import path


from tasks_board.views import (
    all_tasks, sign_up, sign_in, sign_out, current_day, upcoming
)


app_name = 'board'

urlpatterns = [
    path('signout', sign_out, name='sign_out'),
    path('signin/', sign_in, name='sign_in'),
    path('signup/', sign_up, name='sign_up'),
    path('', current_day, name='today'),
    path('tasks/', all_tasks, name='tasks'),
    path('upcoming/', upcoming, name='upcoming'),
]