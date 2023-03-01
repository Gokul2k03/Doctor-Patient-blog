from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_doc, name="register"),
    path('registerpat/', views.register_pat, name='registerpat'),
    path('login/', views.login, name='login'),
    path('blogs/', views.blogsall, name='blogs'),
    path('drafts/', views.drafts, name='drafts'),
    path('myblog/', views.myblogs, name='myblogs'),
    path('create/', views.createBlog, name='create'),
    path('mhealth/', views.mhealth, name='mhealth'),
    path('heartdis/', views.heartdis, name='heartdis'),
    path('covid19/', views.covid19, name='covid19'),
    path('immun/', views.immun, name='immun'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout')
]
