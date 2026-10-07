from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('contacto/nuevo/', views.anadir_contacto, name='anadir_contacto'),

    path('login/', auth_views.LoginView.as_view(
        template_name='contactos/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contacto/<int:id>/', views.detalle_contacto, name='detalle_contacto'),
    path(
        'contacto/<int:id>/editar/',
        views.editar_contacto,
        name='editar_contacto'
    ),
    path(
        'contacto/<int:id>/eliminar/',
        views.eliminar_contacto,
        name='eliminar_contacto'
    ),
    path('registro/', views.registro, name='registro'),

]