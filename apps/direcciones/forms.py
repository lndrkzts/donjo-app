from django.forms import ModelForm

from .models import Direccion


class DireccionForm(ModelForm):
    class Meta:
        model = Direccion
        fields = ['nombre_calle', 'numero_calle', 'barrio', 'observaciones']
        labels = {
            'nombre_calle': 'Calle',
            'numero_calle': 'Número',
            'barrio': 'Barrio',
            'observaciones': 'Observaciones',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre_calle'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['numero_calle'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['barrio'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['observaciones'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ej: Timbre, entre calles, color de la puerta...'
        })
