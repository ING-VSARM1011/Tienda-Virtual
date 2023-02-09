from django.core.validators import MinValueValidator, MaxValueValidator

from Administracion.models import ModeloBase, Producto

from django.db import models
from django.contrib.auth.models import User


class OrdenCompra(ModeloBase):
    codigo = models.CharField(max_length=30, verbose_name='Código', null=False, blank=False)
    cliente = models.ForeignKey(User, verbose_name='Cliente', on_delete=models.RESTRICT, null=False,
                                blank=False)
    direccion = models.TextField(max_length=300, verbose_name='Dirección', null=False, blank=False)
    celular = models.CharField(max_length=10, verbose_name='Celular', null=True, blank=True)
    fecha_entrega = models.DateTimeField(auto_now=True)
    observacion = models.TextField(max_length=500, verbose_name='Observación', null=False, blank=False)
    estado = models.BooleanField(default=True, verbose_name='Estado', null=False, blank=False)
    motivo = models.TextField(max_length=1000, verbose_name='Motivo', null=False, blank=False)

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = 'Orden Compra'


class ProductoOrden(models.Model):
    id = models.BigAutoField(primary_key=True)
    producto = models.ForeignKey(Producto, verbose_name='Producto', on_delete=models.RESTRICT, null=False,
                                 blank=False)
    orden_compra = models.ForeignKey(OrdenCompra, verbose_name='Orden de Compra', on_delete=models.CASCADE, null=False,
                                     blank=False)
    precio = models.DecimalField(default=0, verbose_name='Precio', max_digits=9, decimal_places=2, null=False,
                                 blank=False)
    unidades = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                           verbose_name='Unidades', null=False, blank=False)
    precio_total = models.DecimalField(default=0, verbose_name='Precio Total', max_digits=10, decimal_places=2,
                                       null=False, blank=False)

    def __str__(self):
        return f'Producto: {self.producto.nombre} - Orden de Compra: {self.orden_compra.codigo}'

    class Meta:
        verbose_name = 'ProductoOrden'
