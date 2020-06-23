from django.urls import path
from . import views

app_name = 'userprofile'
urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/',views.user_register, name='register'),
    path('deleta/<int:id>', views.user_delete, name='delete'),
]