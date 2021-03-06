"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path("register", registerPage, name="register"),
    path("login", loginPage, name="login"),
    path("logout", logoutUser, name="logout"),
    path("", TaskList.as_view(), name="home"),
    path("task/<int:pk>", TaskDetail.as_view(), name="task"),
    path("task-create", TaskCreate.as_view(), name="task-create"),
    path("task-update/<int:pk>", TaskUpdate.as_view(), name="task-update"),
    path("task-delete/<int:pk>", DeleteView.as_view(), name="task-delete"),
    path("admin_view", AdminView.as_view(), name="adview")
]
