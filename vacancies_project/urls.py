"""vacancies_project URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static

from vacancies.views import MainView, SpecialVacancyView, AllVacancyView, VacancyView, CompanyView, \
    custom_handler404, custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('vacancies/', AllVacancyView.as_view()),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/cat/<str:specialty_code>/', SpecialVacancyView.as_view()),
    path('companies/<int:company_id>/', CompanyView.as_view(), name='company'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
