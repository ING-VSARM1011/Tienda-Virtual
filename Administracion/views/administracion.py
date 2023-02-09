from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View

from Administracion.general.funciones_validadoras import validar_correo


class IniciarSesionView(View):
    def get(self, request):
        logout(request)
        return render(request, 'administracion/iniciar_sesion.html')

    def post(self, request):
        if not request.user.is_authenticated:
            username = request.POST.get('user')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('administracion:panel-inicio')
            else:
                return render(request, 'administracion/iniciar_sesion.html', {'error': 'El usuario y/o la contraseña no son validos.'})
        else:
            return render(request, 'administracion/panel_inicio.html')


class RegistrarseView(View):
    def get(self, request):
        return render(request, 'administracion/registrarse.html')

    def post(self, request):
        datos = request.POST
        nombres = datos.get('nombres')
        apellidos = datos.get('apellidos')
        username = datos.get('usuario')
        password = datos.get('password')
        correo = datos.get('correo')
        data = {}
        if not validar_correo(correo):
            data.update({'usuario': username, 'password': password, 'correo': correo})
            data.update({'estado_mensaje': 'fallido'})
            return render(request, 'administracion/registrarse.html', data)
        else:
            user = User.objects.create_user(username, correo, password)
            user.is_active = True
            user.first_name = nombres
            user.last_name = apellidos
            user.save()
            data.update({'estado_mensaje': 'exitoso'})
            return render(request, 'administracion/registrarse.html', data)


class CerrarSesionView(View):
    def get(self, request):
        logout(request)
        return redirect('administracion:iniciar-sesion')


class PanelInicioView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'administracion/panel_inicio.html', {'usuario': User.objects.get(id=request.user.id)})
        else:
            return redirect('administracion:iniciar-sesion')



