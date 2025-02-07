from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import*
from .forms import*

def donacion(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'donation_success.html')
    else:
        form = DonationForm()
    return render(request, 'donacion.html', {'form': form})
# Create your views here.
def index(request):
    # proyecto = Proyecto.objects.filter(publicar=True)
    # return render(request, 'index.html', {'proyecto': proyecto})
    # Obtenemos todas las categorías
    categorias = Categoria.objects.all()

    # Crear un diccionario donde las claves son las categorías y los valores los proyectos publicados filtrados
    proyecto = {
        categoria: Proyecto.objects.filter(categoria=categoria, publicar=True)
                                   .order_by('-fecha_creacion')[:6]
        for categoria in categorias
    }

    return render(request, 'index.html', {
        'proyecto': proyecto
    })

    #return render(request, 'index.html')
    
def donar(request):
    return render(request, 'donacion.html')

#def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f'Username: {username}, Password: {password}')  # Verifica los datos
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print('Usuario autenticado')  # Verifica si la autenticación fue exitosa
            login(request, user)
            return redirect('dashboard')
        else:
            print('Usuario o contraseña incorrectos')  # Verifica si la autenticación falló
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')

def home_view(request):
    # Extraer la cantidad de proyectos
    total_proyectos = Proyecto.objects.count()

    # Crear los datos para el gráfico de barras
    datos = {
        'labels': ['Proyectos'],
        'data': [total_proyectos],
    }

    # Pasar los datos al template
    context = {
        'datos': datos
    }
    return render(request, 'dashboard.html')

#def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige a la página de login

# Crear un nuevo proyecto
def proyecto_create(request):
    if request.method == 'POST':
        form = FormularioProyecto(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('dashboard')
       
    else:
        form = FormularioProyecto()
    form_categoria = FormularioCategoria()
    return render(request, 'agregar.html', {'form': form })


# Listar todos los items

def proyecto_list(request):
    proyecto = Proyecto.objects.all()
    categoria_id = request.GET.get('categoria', None)

    if categoria_id:
        proyectos = Proyecto.objects.filter(categoria_id=categoria_id)
    else:
        proyectos = Proyecto.objects.all()  # Si no se selecciona ninguna categoría, muestra todos los proyectos
    
    context = {
        'proyectos': proyectos,
        'categorias': proyecto,
        'categoria_seleccionada': categoria_id
    }
    return render(request, 'listar.html', {'proyecto': proyecto})
    

#editar proyectos
def proyecto_update(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk) #Devuelve un objeto especificado de un modelo en función de su valor de clave principal y genera una excepción Http404 (not found) si el registro no existe
    if request.method == 'POST':
        form = FormularioProyecto(request.POST, request.FILES, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('lista')
    else:
        form = FormularioProyecto(instance=proyecto)
    return render(request, 'agregar.html', {'form': form})

# Publicar un ítem
def publicar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    proyecto.publicar = True
    proyecto.save()
    return redirect('lista')

# Dejar de publicar un ítem
def no_publicar(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    proyecto.publicar = False
    proyecto.save()
    return redirect('lista')
# Agregar categoría

def clean_nueva_categoria(self):
    nueva_categoria = self.cleaned_data.get('nueva_categoria')
    if nueva_categoria and Categoria.objects.filter(nombre=nueva_categoria).exists():
        raise forms.ValidationError('La categoría ya existe.')
    return nueva_categoria


def agregar_categoria(request):
    if request.method == 'POST':
        form = FormularioCategoria(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregar_categoria')  # Redirigir para evitar reenvío del formulario
    else:
        form = FormularioCategoria()

    categorias = Categoria.objects.all()  # Para mostrar todas las categorías existentes
    return render(request, 'agregar_categoria.html', {'form': form, 'categorias': categorias})

def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    return HttpResponseRedirect(reverse('agregar_categoria'))  # Redirige a la lista de categorías