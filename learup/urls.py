"""learup URL Configuration

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
from django.urls import include, path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name='index'),
    path('detail_employ/<int:employ_id>/', views.detail_employ, name='detail employ'),
    path('crear_empleado/', views.crear_empleado, name='crear empleado'),
    path('listar_jerarquia/', views.listar_jerarquias, name='listar jerarquia'),
    path('cambiar_jerarquia/', views.cambiar_jerarquias, name='cambiar jerarquia'),
]