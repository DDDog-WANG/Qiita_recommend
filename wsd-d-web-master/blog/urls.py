
from django.urls import path
from . import views
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('recommend/pattern2', views.read_vec50, name='vec50'),
    path('recommend/pattern1', views.read_vec60, name='vec60'),
]