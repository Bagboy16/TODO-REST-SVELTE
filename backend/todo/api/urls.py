from django.urls import path
from todo.api.api import *

urlpatterns = [
    path('users/', user_api_view, name = 'get_all_users'),
    path('users/<int:user_id>', user_detail_api_view, name = 'user_detail'),
    path('task/', task_api_view, name = 'get_all_tasks'),
    path('task/<int:task_id>', task_detail_api_view, name = 'task_detail')
]