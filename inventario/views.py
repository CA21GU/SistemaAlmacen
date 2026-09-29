from django.contrib import messages
from django.db import models, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm, VentaForm
from .models import Producto, Venta, DetalleVenta


@login_required
def inicio(request):
    productos = Producto.objects.filter(activo=True)

    total_productos = productos.count()

    productos_stock_bajo = productos.filter(
        stock__lte=models.F('stock_minimo')
    ).count()

    ventas = Venta.objects.all()[:5]

    contexto = {
        'total_productos': total_productos,
        'productos_stock_bajo': productos_stock_bajo,
        'ventas': ventas,
    }

    return render(request, 'inventario/inicio.html', contexto)

@login_required
def productos(request):
    lista_productos = Producto.objects.all()

    return render(
        request,
        'inventario/productos.html',
        {'productos': lista_productos}
    )

@login_required
def producto_crear(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Producto creado correctamente.'
            )

            return redirect('productos')
    else:
        form = ProductoForm()

    return render(
        request,
        'inventario/producto_form.html',
        {
            'form': form,
            'titulo': 'Agregar producto'
        }
    )

@login_required
def producto_editar(request, producto_id):
    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    if request.method == 'POST':
        form = ProductoForm(
            request.POST,
            instance=producto
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Producto actualizado correctamente.'
            )

            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)

    return render(
        request,
        'inventario/producto_form.html',
        {
            'form': form,
            'titulo': 'Editar producto'
        }
    )

@login_required
def producto_eliminar(request, producto_id):
    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    if request.method == 'POST':
        producto.delete()

        messages.success(
            request,
            'Producto eliminado correctamente.'
        )

        return redirect('productos')

    return render(
        request,
        'inventario/producto_eliminar.html',
        {'producto': producto}
    )

@login_required
def stock_bajo(request):
    productos = Producto.objects.filter(
        activo=True,
        stock__lte=models.F('stock_minimo')
    )

    return render(
        request,
        'inventario/stock_bajo.html',
        {'productos': productos}
    )

@login_required
@transaction.atomic
def registrar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)

        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']

            producto = Producto.objects.select_for_update().get(
                id=producto.id
            )

            if cantidad > producto.stock:
                form.add_error(
                    'cantidad',
                    f'Stock insuficiente. Stock disponible: {producto.stock}.'
                )
            else:
                venta = Venta.objects.create(
                    total=producto.precio * cantidad
                )

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )

                producto.stock -= cantidad
                producto.save()

                messages.success(
                    request,
                    f'Venta #{venta.id} registrada correctamente.'
                )

                return redirect('ventas')
    else:
        form = VentaForm()

    return render(
        request,
        'inventario/venta_form.html',
        {'form': form}
    )

@login_required
def ventas(request):
    lista_ventas = Venta.objects.prefetch_related(
        'detalles__producto'
    )

    return render(
        request,
        'inventario/ventas.html',
        {'ventas': lista_ventas}
    )