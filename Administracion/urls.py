from django.urls import path

from Administracion.views.administracion import IniciarSesionView, RegistrarseView, CerrarSesionView, PanelInicioView
from Administracion.views.categorias import GetDatosCategoriasView, CategoriasView
from Administracion.views.productos import ProductosView, GetDatosProductosView
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
    path('administracion/categorias/index', CategoriasView.as_view(), name='categorias-index'),
    path('administracion/categorias/registro', CategoriasView.as_view(), name='registro-categoria'),
    path('administracion/categorias/registrar', CategoriasView.as_view(), name='registrar-categoria'),
    path('administracion/categorias/<int:id_elemento>/ver', CategoriasView.as_view(), name='ver-categoria'),
    path('administracion/categorias/<int:id_elemento>/editar', CategoriasView.as_view(), name='editar-categoria'),
    path('administracion/categorias/<int:id_elemento>/eliminar', CategoriasView.as_view(), name='eliminar-categoria'),
    path('administracion/categorias/index/get-datos', GetDatosCategoriasView.as_view(), name='get-categorias'),
    path('administracion/productos/index', ProductosView.as_view(), name='productos-index'),
    path('administracion/productos/registro', ProductosView.as_view(), name='registro-producto'),
    path('administracion/productos/registrar', ProductosView.as_view(), name='registrar-producto'),
    path('administracion/productos/<int:id_elemento>/ver', ProductosView.as_view(), name='ver-producto'),
    path('administracion/productos/<int:id_elemento>/editar', ProductosView.as_view(), name='editar-producto'),
    path('administracion/productos/<int:id_elemento>/eliminar', ProductosView.as_view(), name='eliminar-producto'),
    path('administracion/productos/index/get-datos', GetDatosProductosView.as_view(), name='get-productos'),
]