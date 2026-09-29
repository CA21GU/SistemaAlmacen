from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('login/', auth_views.LoginView.as_view(
        template_name='inventario/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('productos/', views.productos, name='productos'),
    path('productos/nuevo/', views.producto_crear, name='producto_crear'),
    path(
        'productos/<int:producto_id>/editar/',
        views.producto_editar,
        name='producto_editar'
    ),
    path(
        'productos/<int:producto_id>/eliminar/',
        views.producto_eliminar,
        name='producto_eliminar'
    ),

    path('stock-bajo/', views.stock_bajo, name='stock_bajo'),

    path('ventas/', views.ventas, name='ventas'),
    path('ventas/nueva/', views.registrar_venta, name='registrar_venta'),
]