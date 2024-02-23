from django.urls import path
from .import views
from app_album_viewer import views as views2

urlpatterns = [
     path('', views.home, name='home'),
     path('about', views.about, name='about'),
     path('contact', views.contact, name='contact'),
     path('albums', views2.album_list , name='albums'),
     path('signup', views.RegisterUser.as_view(), name='signup_user'),
]