from django.urls import path

from Administracion.views.administracion import IniciarSesionView, RegistrarseView

app_name = 'Administracion'

urlpatterns = [
    path('', IniciarSesionView.as_view(), name='iniciar-sesion'),
    path('registrarse', RegistrarseView.as_view(), name='registrarse'),
]