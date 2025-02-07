from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

#modelo que manaja las donaciones
class Donation(models.Model):
    DONATION_CHOICES = [
        (10, '10 Q'),
        (50, '50 Q'),
        (100, '100 Q'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, choices=DONATION_CHOICES, blank=True, null=True)
    custom_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_receipt = models.FileField(upload_to='boletas/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount or self.custom_amount} Q"

class Categoria(models.Model):
    nombre=models.CharField(max_length=30, blank=True, null=False)
    descripcion=models.CharField(max_length=60, blank=True, null=False)
    def __str__(self):
        return self.nombre

#clase para manejar categorias de proyectos
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='images/')
    publicar=models.BooleanField(default=False, blank=True, null=False)
    fecha_creacion=models.DateField(blank=True, null=False)
    categoria=models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    #fecha_actualizacion
   
    # ordenar por categoría y fecha:

    def __str__(self):
        return self.nombre
