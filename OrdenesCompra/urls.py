from django.urls import path

from OrdenesCompra.views.ordenes import OrdenesCompraView, GetDatosOrdenesCompraView

app_name = 'OrdenesCompra'

urlpatterns = [
    path('ordenes-compra/mis-ordenes/index', OrdenesCompraView.as_view(), name='ordenes-compra-index'),
    path('ordenes-compra/mis-ordenes/registro', OrdenesCompraView.as_view(), name='registro-orden-compra'),
    path('ordenes-compra/mis-ordenes/index/get-datos', GetDatosOrdenesCompraView.as_view(), name='get-ordenes-compra'),
]