from django.urls import path

from . import views
from . import rag_views

urlpatterns = [
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('signup', views.signup_view),
    path('check', views.checkAuthentication),
    path('loadContext', rag_views.loadContext),
    path('getContexts', rag_views.getContexts)
]