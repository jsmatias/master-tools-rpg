from django.urls import path, include
# from .views import RegisterView, LoginView, UserView, UpdateUserAPI
from .api import RegisterUserApi, LoginApi, UserApi, UpdateUserAPI, UpdatePassAPI, LogoutAPI
from knox import views as knox_views

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterUserApi.as_view(), name='register-user'),
    path('api/auth/login', LoginApi.as_view(), name='login'),
    path('api/auth/user', UserApi.as_view(), name='get-current-user'),
    path('api/auth/update', UpdateUserAPI.as_view(), name='update-user'),
    path('api/auth/change-password',
         UpdatePassAPI.as_view(), name='change-password'),
    path('api/auth/logout', LogoutAPI.as_view(), name='logout'),
]
