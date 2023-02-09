from django.urls import path

from Administracion.views.administracion import IniciarSesionView, RegistrarseView, CerrarSesionView, PanelInicioView
from Administracion.views.usuarios import UsuariosView

app_name = 'Administracion'

urlpatterns = [
    path('', IniciarSesionView.as_view(), name='iniciar-sesion'),
    path('registrarse', RegistrarseView.as_view(), name='registrarse'),
    path('cerrar-sesion', CerrarSesionView.as_view(), name='cerrar-sesion'),
    path('panel-inicio', PanelInicioView.as_view(), name='panel-inicio'),
    path('administracion/usuarios/index', UsuariosView.as_view(), name='usuarios-index'),
    path('administracion/usuarios/<int:id_elemento>/ver', UsuariosView.as_view(), name='ver-usuario'),
    path('administracion/usuarios/<int:id_elemento>/editar', UsuariosView.as_view(), name='editar-usuario'),
    path('administracion/usuarios/<int:id_elemento>/eliminar', UsuariosView.as_view(), name='eliminar-usuario'),
]