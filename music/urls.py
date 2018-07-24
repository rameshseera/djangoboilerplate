from django.urls import path
from . import views

app_name='music'

urlpatterns = [
    path('', views.index, name='index'),
    path('tell/', views.tell, name='tell'),
    path('albums/', views.albums, name='songs'),
    path('albums/', views.albums, name='create_album'),
    #url(r'^album/(?P<album_id>[0-9]{4})/$', views.details)
    path('album/<int:album_id>',views.details, name='details'),
    path('song/<int:song_id>',views.details, name='song_details'),
    path('list/',views.IndexView.as_view(), name='index'),
    path('list/album/<int:pk>',views.DetailView.as_view(), name='song_details'),
    path('register/',views.UserFormView.as_view(), name='register'),
    path('login/',views.login_user, name='login_user'),
    path('login/',views.login_user, name='logout_user'),
]