"""E_Commerce URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Administracion.urls', namespace='administracion')),
    path('', include('OrdenesCompra.urls', namespace='ordenes-compra')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
