from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from E_Commerce.general.controlador_views import GeneralView
from E_Commerce.general.json_model import RespuestaJson


class UsuariosView(GeneralView):
    def index(self, request):
        usuarios = User.objects.filter(is_active=True, is_superuser=False).order_by('-date_joined') \
            if User.objects.filter(is_active=True, is_superuser=False).exists() else []

        return render(request, 'usuarios/index.html', {
            'usuario': User.objects.get(id=request.user.id),
            'usuarios': usuarios,
            'estado_mensaje': '',
            'fecha': datetime.now(),
        })

    def ver(self, request, id_elemento):
        return render(request, 'usuarios/_editar_modal.html', {
            'usuario': User.objects.get(id=id_elemento),
            'fecha': datetime.now(),
        })

    def editar(self, request, id_elemento):
        data = request.POST
        usuario_db = User.objects.get(id=id_elemento)

        usuario_db.first_name = data.get('nombres')
        usuario_db.last_name = data.get('apellidos')
        usuario_db.email = data.get('correo')
        usuario_db.username = data.get('usuario')
        usuario_db.password = make_password(data.get('password'))

        usuario_db.save(update_fields=['first_name', 'last_name', 'email', 'username', 'password'])

        return redirect('administracion:usuarios-index')

    def eliminar(self, request, id_elemento):
        ruta_redireccion = '' if id_elemento == request.user.id else '/administracion/usuarios/index'
        usuario = User.objects.get(id=id_elemento)
        usuario.is_active = False
        usuario.save(update_fields=['is_active'])

        return RespuestaJson.exitosa(datos={'titulo': 'Usuario Eliminado!!!',
                                            'mensaje': f'Se ha eliminado el usuario {usuario.username}',
                                            'icono': 'success', 'ruta': ruta_redireccion})



