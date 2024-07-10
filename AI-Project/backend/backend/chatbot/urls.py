from django.urls import path

from . import views
from . import rag_views

urlpatterns = [
    path('login', views.login_view),
    path('extlogin', views.login_ext_view),
    path('logout', views.logout_view),
    path('signup', views.signup_view),
    path('check', views.checkAuthentication),
    path('loadContext', rag_views.loadContext),
    path('loadSharepoint', rag_views.loadSharepoint),
    path('addModel', rag_views.addModel),
    path('getContexts', rag_views.getContexts),
    path('getModels', rag_views.getModels),
    path('queryChatbot', rag_views.query)
]