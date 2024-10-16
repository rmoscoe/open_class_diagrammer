"""
URL configuration for open_class_diagrammer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from class_manager.views import HomePageView, SignupView, OpenClassDiagrammerLoginView, UserUpdateView, UserDetailView, WorkbenchView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("class-manager/", include("class_manager.urls")),
    path("", HomePageView.as_view(), name="home"),
    path("account/register/", SignupView.as_view(), name="register"),
    path("account/login", OpenClassDiagrammerLoginView.as_view(), name="login"),
    path("account/<pk>/update/", UserUpdateView.as_view(), name="account-update"),
    path("account/<pk>/details/", UserDetailView.as_view(), name="account-detail"),
    path("workbench/", WorkbenchView.as_view(), name="workbench"),
    path("__reload__/", include("django_browser_reload.urls"))
]
