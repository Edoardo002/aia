from django.urls import path

from . import views

urlpatterns = [
    path("query", views.queryChatbot),
    path("setup", views.loadData),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('signup', views.signup_view),
    path('check', views.checkAuthentication)
]