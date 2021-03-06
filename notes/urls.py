"""notes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from api import views as api_views
from app import views as app_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path


schema_view = get_schema_view(
   openapi.Info(
      title="Note API",
      default_version='v0.0.1',
      description="ReciprocIT back-end test",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
	re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
	re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
 
    path('admin/', admin.site.urls),
    
    # API VIEWS
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/account/logout/', api_views.LogoutView.as_view(), name='logout'),
    path('api/notesList/', api_views.NotesList.as_view()),
    path('api/noteAdd/', api_views.NoteAdd.as_view()),
    path('api/noteDetail/<uuid:pk>/', api_views.NoteDetail.as_view()),
    path('api/noteUpdate/<uuid:pk>/', api_views.NoteUpdate.as_view()),
    path('api/account/register/', api_views.RegistrationView.as_view(), name='register'),
    path('api/account/login/', api_views.LoginView.as_view(), name='login'),
    
    # APP VIEWS
    path('', app_views.homePageView, name='index'),
    path('notes/', app_views.NotesView, name='notes'),
    path('register/', app_views.RegisterView, name='register'),
]
