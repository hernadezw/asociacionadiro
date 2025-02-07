from django.contrib import admin
from django.urls import path
from .views import*

urlpatterns = [
    path('', index,  name="index" ),
    path('donacr/', donacion, name="donar" ),
    
    #path('login/', login_view, name='log'),
    path('home/', home_view, name='dashboard'),

    path('home/lista/', proyecto_list, name='lista'),

   # path('logout/', logout_view, name='logout'),
    path('home/create', proyecto_create, name='crear'),
    path('home/<int:pk>/edit/', proyecto_update, name='actualizar'),

    path('home/<int:pk>/publicar/', publicar_proyecto, name='publicar'),
    path('home/<int:pk>/dejar_de_publicar/', no_publicar, name='no_publicar'),

    path('home/agregar-categoria/', agregar_categoria, name='agregar_categoria'),
    path('home/agregar-categoria/<int:categoria_id>/', eliminar_categoria, name='eliminar_categoria'),
    #path('agregar-categoria-ajax/', agregar_categoria_ajax, name='agregar_categoria_ajax')
   
    
]