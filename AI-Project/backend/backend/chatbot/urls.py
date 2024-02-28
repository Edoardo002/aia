from django.urls import path

from . import views

urlpatterns = [
    path("/query", views.queryChatbot, name="queryChatbot"),
    path("/setup", views.loadData, name="loadData"),
    path("/login", views.login, name="userLogin"),
]