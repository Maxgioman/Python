from django.urls import path

from . import views
from django.urls import include, path, re_path

# /playlist
# /user/<id>

urlpatterns = [
    path('index/', views.index, name='index'), # page
    re_path('^index/registration/', views.registration),
    path('login/', views.login), # page
    path('logout/', views.logout),
    path('user/playlist', views.userlist), # page userId=1&playlistId=2
    path('userlist/track/', views.addTrack), #page
    re_path('^userlist/track/add/', views.addTrack), 
    re_path('^userlists/delete/', views.userlists),  # page -_-
    re_path('^userlists/create/add/', views.addPlaylist),
    re_path('^userlists/create/', views.addPlaylist),
    path('user/playlist/modify/', views.modify_pl),
    path('user/playlist/modify/add/', views.modify_pl),
    path('user/playlist/modify/put/', views.mod_put),
    path('user/playlist/modify/put/put/', views.mod_put)
]
