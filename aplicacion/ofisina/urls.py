from django.urls import path
from . import views

urlpatterns = [
    # Página de inicio
    path('', views.inicio),

    # OFICINA
    path('nuevaoficina/', views.nuevaoficina),  # Formulario para agregar nuevo abogado
    path('listaoficina/', views.listaoficina),  # Listado de abogados
    path('guardaroficina/', views.guardaroficina),  # Guardar nuevo abogado
    path('editaroficina/<oficina_id>', views.editaroficina),  # Editar abogado
    path('procesarEdicionoficina/', views.procesarEdicionoficina),  # Procesar edición de abogado
    path('eliminaroficina/<oficina_id>', views.eliminaroficina),  # Eliminar abogado


    # CONTRATISTA
    path('nuevacontratista/', views.nuevacontratista),  # Formulario para agregar nuevo abogado
    path('listacontratista/', views.listacontratista),  # Listado de abogados
    path('guardarcontratista/', views.guardarcontratista),  # Guardar nuevo abogado
    path('editarcontratista/<contratista_id>', views.editarcontratista),  # Editar abogado
    path('procesarEdicioncontratista/', views.procesarEdicioncontratista),  # Procesar edición de abogado
    path('eliminarcontratista/<contratista_id>', views.eliminarcontratista),  # Eliminar abogado
    

     # REFORMA
    path('nuevareforma/', views.nuevareforma),  # Formulario para agregar queja
    path('listareforma/', views.listareforma),  # Página con el listado de quejas
    path('guardarreforma/', views.guardarreforma),   # Guardar la queja
    path('eliminarreforma/<reforma_id>', views.eliminarreforma),  # Eliminar queja
    path('editarreforma/<reforma_id>', views.editarreforma),  # Editar abogado
    path('procesarEdicionreforma/', views.procesarEdicionreforma),  # Procesar edición de abogado
      # SUMINISTRO
    path('nuevasuministro/', views.nuevasuministro),  # Formulario para agregar nuevo abogado
    path('listasuministro/', views.listasuministro),  # Listado de abogados
    path('guardarsuministro/', views.guardarsuministro),  # Guardar nuevo abogado
    path('editarsuministro/<suministro_id>', views.editarsuministro),  # Editar abogado
    path('procesarEdicionsuministro/', views.procesarEdicionsuministro),  # Procesar edición de abogado
    path('eliminarsuministro/<suministro_id>', views.eliminarsuministro),  # Eliminar abogado
    
    # PDF
    path('pdf/', views.exportar_pdf, name='pdf'),

]