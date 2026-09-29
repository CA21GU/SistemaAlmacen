from django.contrib import admin
from .models import Producto, Venta, DetalleVenta


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'categoria',
        'precio',
        'stock',
        'stock_minimo',
        'activo',
    )

    list_filter = (
        'categoria',
        'activo',
    )

    search_fields = (
        'nombre',
        'categoria',
    )

    ordering = (
        'nombre',
    )


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fecha',
        'total',
    )

    inlines = [
        DetalleVentaInline,
    ]


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = (
        'venta',
        'producto',
        'cantidad',
        'precio_unitario',
    )

    list_filter = (
        'producto',
    )