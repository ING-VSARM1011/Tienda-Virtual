from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class ModeloBase(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_modifica = models.IntegerField(verbose_name='Usuario Modifica', null=False, blank=False)
    usuario_crea = models.IntegerField(verbose_name='Usuario crea', null=False, blank=False)

    def __str__(self):
        return self

    class Meta:
        verbose_name = 'Modelo Base'
        abstract = True


class Categoria(ModeloBase):
    nombre = models.TextField(max_length=100, verbose_name='Nombre', null=False, blank=False)
    descripcion = models.TextField(max_length=1000, verbose_name='Descripción', null=False, blank=False)
    imagen = models.CharField(max_length=60, verbose_name='Imagen', null=False, blank=False)
    estado = models.BooleanField(default=True, verbose_name='Estado', null=False, blank=False)
    motivo = models.TextField(max_length=1000, verbose_name='Descripción', null=False, blank=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Categoria'

    @staticmethod
    def from_instance(data: dict, id_user) -> 'Categoria':
        categoria = Categoria()
        categoria.nombre = data.get('nombre', '')
        categoria.descripcion = data.get('descripcion', '')
        categoria.motivo = data.get('motivo', '')
        categoria.imagen = data.get('imagen', 'categoria-ropa-mujer.jpg')
        categoria.usuario_crea = categoria.usuario_modifica = id_user

        return categoria


class Producto(ModeloBase):
    codigo = models.CharField(max_length=30, verbose_name='Código', null=False, blank=False)
    nombre = models.TextField(max_length=500, verbose_name='Nombre', null=False, blank=False)
    descripcion = models.TextField(max_length=1000, verbose_name='Descripción', null=False, blank=False)
    marca = models.CharField(max_length=50, verbose_name='Marca', null=False, blank=False)
    precio = models.DecimalField(default=0, verbose_name='Precio', max_digits=8, decimal_places=2, null=False,
                                 blank=False)
    cantidad_disponible = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0),
                                                                             MaxValueValidator(100)],
                                                      verbose_name='Cantidad Disponible', null=False,
                                                      blank=False)
    estado = models.BooleanField(default=True, verbose_name='Estado', null=False, blank=False)
    motivo = models.TextField(max_length=1000, verbose_name='Descripción', null=False, blank=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Producto'


class ProductoCategoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    producto = models.ForeignKey(Producto, verbose_name='Producto', on_delete=models.RESTRICT, null=False,
                                 blank=False)
    categoria = models.ForeignKey(Categoria, verbose_name='Categoria', on_delete=models.CASCADE, null=False,
                                  blank=False)

    def __str__(self):
        return f'Producto: {self.producto.nombre} - Categoria: {self.categoria.nombre}'

    class Meta:
        verbose_name = 'ProductoCategoria'
