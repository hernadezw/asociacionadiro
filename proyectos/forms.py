from django import forms
from .models import Proyecto, Categoria, Donation

class FormularioProyecto(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'imagen','publicar','fecha_creacion', 'categoria']
        
        widgets = {
            'fecha_creacion': forms.DateInput(attrs={'type': 'date'}),
            
        }

class FormularioCategoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['name', 'email', 'amount', 'custom_amount', 'payment_receipt']
        labels = {
            'name': 'Nombre completo',
            'email': 'Correo electrónico (no necesario)',
            'amount': 'Monto fijo',
            'custom_amount': 'Monto personalizado',
            'payment_receipt': 'Subir boleta de depósito',
        }

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        custom_amount = cleaned_data.get('custom_amount')
        if not amount and not custom_amount:
            raise forms.ValidationError("Debes elegir un monto fijo o ingresar uno personalizado.")
        return cleaned_data