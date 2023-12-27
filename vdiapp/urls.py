from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework.authtoken import views

urlpatterns = [
    path('create-vdi/', view=CreateVDI.as_view(), name='create-vdi'),
    path('create-hd/', view=CreateHD.as_view(), name='create-hd'),
    path('create-user/', view=CreateUser.as_view(), name='create-user'),
    path('update-hd/<int:pk>/', view=UpdateHD.as_view(), name='update-hd'),
    path('update-user/<int:pk>/', view=UpdateUser.as_view(), name='update-user'),
    path('update-vdi/<str:pk>/', view=UpdateVDI.as_view(), name='update-vdi'),
    path('get-all-vdi/', view=GetAllMachines.as_view(), name='get-all-vdi'),
    path('get-all-active-vdi/', view=GetAllActiveMachines.as_view(), name='get-all-active-vdi'),
    path('get-all-users/', view=GetAllUsers.as_view(), name='get-all-users'),
    path('get-user-vdi/', view=GetAllUserMachines.as_view(), name='get-user-vdi'),
    path('connect-vdi/<str:pk>/', view=VdiConnect.as_view(), name='connect-vdi'),
    path('disconnect-vdi/<str:pk>/', view=VdiDisconnect.as_view(), name='disconnect-vdi'),
    path('delete-vdi/<str:pk>/', view=DeleteVdi.as_view(), name='delete-vdi'),
    path('get-stats/', view=GetStatisic.as_view(), name='get-stats'),

]

urlpatterns += [
    path('api-token-login/', views.obtain_auth_token, name='api-token-login'),
    path('api-token-logout/', Logout.as_view(), name='api-token-logout'),

]