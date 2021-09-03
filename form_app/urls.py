from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.loginPage, name="login"),
  path('logout/', views.logoutPage, name="logout"),
  path('', views.mainPage, name="main"),
  path('form/<str:form_id>/', views.formPage, name="form"),
  path('stats/', views.statsPage, name="stats"),
  path('form_stats/<str:form_id>/', views.formStatsPage, name="form_stats"),
  path('open_forms/<str:type_id>/', views.openFormsPage, name="open_forms"),
  path('close_forms/<str:type_id>/', views.closeFormsPage, name="close_forms")
]