from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from E_Commerce.general.controlador_views import GeneralView
from OrdenesCompra.models import OrdenCompra


class OrdenesCompraView(GeneralView):
    def index(self, request):
        if request.user.is_authenticated:
            return render(request, 'ordenes/index.html', {'fecha': datetime.now()})
        else:
            return redirect('administracion:iniciar-sesion')


class GetDatosOrdenesCompraView(View):
    def post(self, request):
        indice_reg_inicial = int(request.POST['start'])
        indice_reg_final = indice_reg_inicial + int(request.POST['length'])
        list_ordenes = []
        filtro = {'estado': True}

        total_ordenes = OrdenCompra.objects.filter(**filtro).order_by('-fecha_creacion')
        ordenes = total_ordenes[indice_reg_inicial:indice_reg_final]
        for reg in ordenes:
            ruta_editar = f'/ordenes-compra/mis-ordenes/{reg.id}/ver'
            id_modal_editar = f'registrar-editar-orden-compra'
            form_editar = f'form-registrar-editar-orden-compra'
            href_editar = f"Javascript:abrirModal('{ruta_editar}'," + f"'{id_modal_editar}','{form_editar}')"
            href_eliminar = f"Javascript:eliminarElemento('/ordenes-compra/mis-ordenes/','Compra'," + f"{reg.id})"
            datos = ['', reg.codigo, reg.fecha_entrega.strftime('%Y-%m-%d'), reg.observacion, reg.direccion,
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
                     f'<line x1="14" y1="11" x2="14" y2="17"></line></svg></a>', reg.celular,
                     reg.fecha_creacion.strftime('%Y-%m-%d')]

            list_ordenes.append(datos)
        list_data = {"draw": int(request.POST['draw']), "recordsTotal": len(total_ordenes), "data": list_ordenes,
                     "recordsFiltered": len(total_ordenes)}
        return JsonResponse(list_data, safe=False)
