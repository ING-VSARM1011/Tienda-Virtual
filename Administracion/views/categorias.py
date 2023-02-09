from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from Administracion.models import Categoria
from E_Commerce.general.controlador_views import GeneralView
from E_Commerce.general.json_model import RespuestaJson


class CategoriasView(GeneralView):
    def index(self, request):
        if request.user.is_authenticated:
            return render(request, 'categorias/index.html', {'fecha': datetime.now()})
        else:
            return redirect('administracion:iniciar-sesion')

    def registro(self, request):
        if request.user.is_authenticated:
            return render(request, 'categorias/_registro_editar_modal.html', {
                'editar': False,
                'fecha': datetime.now()
            })
        else:
            return redirect('administracion:iniciar-sesion')

    def registrar(self, request):
        categoria = Categoria.from_instance(request.POST, request.user.id)
        categoria.save()

        return render(request, 'categorias/index.html')

    def ver(self, request, id_elemento):
        categoria = Categoria.objects.get(id=id_elemento)
        return render(request, 'categorias/_registro_editar_modal.html', {
            'categoria': categoria,
            'editar': True,
            'fecha': datetime.now(),
        })

    def editar(self, request, id_elemento):
        data = request.POST
        categoria_db = Categoria.objects.get(id=id_elemento)

        categoria_db.nombre = data.get('nombre')
        categoria_db.descripcion = data.get('descripcion')
        categoria_db.motivo = data.get('motivo')
        categoria_db.fecha_modificacion = datetime.now()
        categoria_db.usuario_modifica = request.user.id

        categoria_db.save(update_fields=['nombre', 'descripcion', 'motivo', 'fecha_modificacion', 'usuario_modifica'])

        return redirect('administracion:categorias-index')

    def eliminar(self, request, id_elemento):
        categoria = Categoria.objects.get(id=id_elemento)
        categoria.usuario_modifica = request.user.id
        categoria.estado = False
        categoria.motivo = request.GET.get('motivo')
        categoria.fecha_modificacion = datetime.now()
        categoria.save(update_fields=['estado', 'motivo', 'fecha_modificacion', 'usuario_modifica'])
        return RespuestaJson.exitosa(datos={'titulo': 'Categoría Eliminada!!!',
                                            'mensaje': f'Se ha eliminado la categoría {categoria.nombre}',
                                            'icono': 'success', 'ruta': '/administracion/categorias/index'})


class GetDatosCategoriasView(View):
    def post(self, request):
        indice_reg_inicial = int(request.POST['start'])
        indice_reg_final = indice_reg_inicial + int(request.POST['length'])
        list_categorias = []
        filtro = {'estado': True}

        total_categorias = Categoria.objects.filter(**filtro).order_by('-fecha_creacion')
        categorias = total_categorias[indice_reg_inicial:indice_reg_final]
        for reg in categorias:
            ruta_editar = f'/administracion/categorias/{reg.id}/ver'
            id_modal_editar = f'registrar-editar-categoria'
            form_editar = f'form-registrar-editar-categoria'
            href_editar = f"Javascript:abrirModal('{ruta_editar}'," + f"'{id_modal_editar}','{form_editar}')"
            href_eliminar = f"Javascript:eliminarElemento('/administracion/categorias/','Categoría'," + f"{reg.id})"
            href_imagen = f"../../static/assets/img/{reg.imagen}"
            datos = ['', reg.nombre, reg.descripcion, 26,
                     f'<a href={href_editar} id="editar_{reg.id}" class="bs-tooltip mr-1" data-bs-toggle="tooltip" data-placement="top" title="Editar">'
                     f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                     f'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
                     f'stroke-linejoin="round" class="feather feather-edit text-info">'
                     f'<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>'
                     f'<path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg></a>'
                     f'<a href={href_eliminar} id="eliminar_{reg.id}" data-toggle="tooltip" data-placement="top" title="Eliminar">'
                     f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                     f'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
                     f'stroke-linejoin="round" class="feather feather-trash-2 text-danger" > '
                     f'<polyline points="3 6 5 6 21 6"></polyline > '
                     f'<path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" > '
                     f'</path><line x1="10" y1="11" x2="10" y2="17"></line> '
                     f'<line x1="14" y1="11" x2="14" y2="17"></line></svg></a>', f'<a target="_blank" '
                                                                                 f'href={href_imagen} '
                                                                                 f'data-bs-toggle="tooltip" '
                                                                                 f'data-bs-placement="top" '
                                                                                 f'title="Ver Imagen"><i>'
                                                                                 f'</i>{reg.imagen}</a>',
                     reg.fecha_creacion.strftime('%Y-%m-%d')]

            list_categorias.append(datos)
        list_data = {"draw": int(request.POST['draw']), "recordsTotal": len(total_categorias), "data": list_categorias,
                     "recordsFiltered": len(total_categorias)}
        return JsonResponse(list_data, safe=False)
