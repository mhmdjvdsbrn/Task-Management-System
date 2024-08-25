# your_app/urls.py
from django.urls import path
from .apis import TaskViewSelector, TaskViewServices

urlpatterns = [
    path('tasks-list/', TaskViewSelector.as_view({'get': 'list'}), name='tasks-list'),
    path('tasks-detail/<int:pk>/', TaskViewSelector.as_view({'get': 'retrieve'}), name='task-detail'),
    path('new_tasks/', TaskViewServices.as_view({'post': 'create'}), name='new-tasks'),
    path('update_tasks/<int:pk>/', TaskViewServices.as_view({'put': 'update'}), name='update-tasks'),
    path('delete_tasks/<int:pk>/', TaskViewServices.as_view({'delete': 'destroy'}), name='delete-tasks'),

]
