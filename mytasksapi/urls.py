from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('register', register, name='register'),
    path('login', login_user, name='login'),
    path('user/logout', logout_user, name='logout'),
    path('tasks/', tasks, name='tasks'),
    path('tasks/<int:task_id>', items, name='items'),
    path('tasks/<int:task_id>/<int:item_id>', item, name='item'),
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
