"""
URL configuration for arabic_dictionary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from dictionary.views import add_word
from dictionary.views import home
from django.contrib import admin
from dictionary.views import word_list
from dictionary.views import signup
from dictionary.views import login_view
from dictionary.views import logout_view
from django.urls import path
from dictionary.views import word_detail
from dictionary import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('add_word/', add_word, name='add_word'),
    path('word/<int:pk>/', word_detail, name='word_detail'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('search/', views.search_results, name='search_results'),
    path('login/', login_view, name='login'),
    path('edit_word/<int:word_id>/', views.edit_word, name='edit_word'),
    path('delete_word/<int:word_id>/', views.delete_word, name='delete_word'),
    path('words/', word_list, name='word_list'),
]
