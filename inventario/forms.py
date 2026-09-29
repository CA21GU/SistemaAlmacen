from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'categoria',
            'precio',
            'stock',
            'stock_minimo',
            'activo',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'categoria': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()

        if not nombre:
            raise forms.ValidationError(
                'El nombre del producto es obligatorio.'
            )

        return nombre

    def clean_precio(self):
        precio = self.cleaned_data['precio']

        if precio <= 0:
            raise forms.ValidationError(
                'El precio debe ser mayor que cero.'
            )

        return precio

    def clean_stock(self):
        stock = self.cleaned_data['stock']

        if stock < 0:
            raise forms.ValidationError(
                'El stock no puede ser negativo.'
            )

        return stock


class VentaForm(forms.Form):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=True),
        empty_label='Seleccione un producto'
    )

    cantidad = forms.IntegerField(
        min_value=1,
        label='Cantidad'
    )