from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import F

from Administracion.models import Categoria, Producto
from Administracion.models.administracion import ProductoCategoria
from E_Commerce.general.controlador_views import GeneralView
from E_Commerce.general.json_model import RespuestaJson


class ProductosView(GeneralView):
    def index(self, request):
        if request.user.is_authenticated:
            return render(request, 'productos/index.html', {'fecha': datetime.now()})
        else:
            return redirect('administracion:iniciar-sesion')

    def registro(self, request):
        if request.user.is_authenticated:
            list_categorias_select = [{'index': categoria.id, 'name': categoria.nombre}
                                      for categoria in Categoria.objects.filter(estado=True)]

            return render(request, 'productos/_registro_editar_modal.html', {
                'categorias_select': list_categorias_select,
                'editar': False,
                'fecha': datetime.now()
            })
        else:
            return redirect('administracion:iniciar-sesion')

    def registrar(self, request):
        producto = Producto.from_instance(request.POST, request.user.id)
        producto.save()

        for nombre_categoria in request.POST.getlist("state[]"):
            categoria = Categoria.objects.get(nombre=nombre_categoria)
            if categoria:
                producto_categoria = ProductoCategoria()
                producto_categoria.producto = producto
                producto_categoria.categoria = categoria
                producto_categoria.save()
        return render(request, 'productos/index.html')

    def ver(self, request, id_elemento):
        producto = Producto.objects.get(id=id_elemento)
        list_categorias_select = [{'index': categoria.id, 'name': categoria.nombre}
                                  for categoria in Categoria.objects.filter(estado=True)]
        return render(request, 'productos/_registro_editar_modal.html', {
            'producto': producto,
            'categorias_select': list_categorias_select,
            'editar': True,
            'fecha': datetime.now(),
        })

    def editar(self, request, id_elemento):
        data = request.POST
        producto_db = Producto.objects.get(id=id_elemento)

        producto_db.codigo = data.get('codigo')
        producto_db.nombre = data.get('nombre')
        producto_db.descripcion = data.get('descripcion')
        producto_db.marca = data.get('marca')
        producto_db.precio = data.get('precio')
        producto_db.cantidad_disponible = data.get('cantidad')

        producto_db.motivo = data.get('motivo')
        producto_db.fecha_modificacion = datetime.now()
        producto_db.usuario_modifica = request.user.id

        producto_db.save(update_fields=['codigo', 'nombre', 'descripcion', 'marca', 'precio', 'cantidad_disponible',
                                        'motivo', 'fecha_modificacion', 'usuario_modifica'])

        return redirect('administracion:categorias-index')

    def eliminar(self, request, id_elemento):
        producto = Producto.objects.get(id=id_elemento)
        producto.usuario_modifica = request.user.id
        producto.estado = False
        producto.motivo = request.GET.get('motivo')
        producto.fecha_modificacion = datetime.now()
        producto.save(update_fields=['estado', 'motivo', 'fecha_modificacion', 'usuario_modifica'])
        return RespuestaJson.exitosa(datos={'titulo': 'Producto Eliminado!!!',
                                            'mensaje': f'Se ha eliminado el producto {producto.nombre}',
                                            'icono': 'success', 'ruta': '/administracion/productos/index'})


class GetDatosProductosView(View):
    def post(self, request):
        indice_reg_inicial = int(request.POST['start'])
        indice_reg_final = indice_reg_inicial + int(request.POST['length'])
        list_productos = []
        filtro = {'estado': True}

        total_productos = Producto.objects.filter(**filtro).order_by('-fecha_creacion')
        productos = total_productos[indice_reg_inicial:indice_reg_final]
        for reg in productos:
            categorias_producto = ProductoCategoria.objects.filter(producto_id=reg.id)\
                .annotate(nombre_categoria=F('categoria_id__nombre'))
            categorias = [categoria.nombre_categoria for categoria in categorias_producto]
            ruta_editar = f'/administracion/productos/{reg.id}/ver'
            id_modal_editar = f'registrar-editar-producto'
            form_editar = f'form-registrar-editar-producto'
            href_editar = f"Javascript:abrirModal('{ruta_editar}'," + f"'{id_modal_editar}','{form_editar}')"
            href_eliminar = f"Javascript:eliminarElemento('/administracion/productos/','Producto'," + f"{reg.id})"
            href_imagen = f"../../static/assets/img/{reg.imagen}"
            datos = ['', reg.codigo, reg.nombre, reg.descripcion, "{}{:,.2f}".format('$', reg.precio),
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
                     f'{categorias}'.replace('[', '').replace(']', ''), reg.marca, 26, reg.fecha_creacion.strftime('%Y-%m-%d')]

            list_productos.append(datos)
        list_data = {"draw": int(request.POST['draw']), "recordsTotal": len(total_productos), "data": list_productos,
                     "recordsFiltered": len(total_productos)}
        return JsonResponse(list_data, safe=False)
