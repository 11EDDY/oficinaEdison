from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contratista, Oficina, Reforma, Suministro
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from reportlab.lib.utils import simpleSplit
from django.core.mail import EmailMessage
# Vista de inicio
def inicio(request):
    return render(request, 'inicio.html')

# Contratista -------------------------------------------------------------------------------------------------

# Vista para mostrar el formulario de nuevo Contratista
def nuevacontratista(request):
    return render(request, 'nuevacontratista.html')

# Vista para mostrar la lista de Contratistas
def listacontratista(request):
    contratistas = Contratista.objects.all()
    return render(request, 'listacontratista.html', {'contratistas': contratistas})

# Vista para guardar un nuevo Contratista

def guardarcontratista(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST['txt_nombre']
        telefono = request.POST['txt_telefono']
        email = request.POST['txt_correo']

        # Crear el nuevo contratista
        nuevo_contratista = Contratista.objects.create(
            nombre=nombre,
            telefono=telefono,
            email=email
        )

        # Enviar correo de confirmación
        subject = "Registro de Contratista Exitoso"
        message = f"Hola {nombre},\n\nTu registro como contratista ha sido exitoso.\n\nDetalles:\nNombre: {nombre}\nTeléfono: {telefono}\nCorreo: {email}\n\nGracias por unirte a nuestra comunidad."
        from_email = 'tu-email@gmail.com'  # Cambia esto por tu correo real
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            messages.success(request, "Contratista Guardado Exitosamente y correo enviado")
        except Exception as e:
            messages.error(request, f"Contratista guardado, pero hubo un error al enviar el correo: {str(e)}")

        # Redirigir a la lista de contratistas
        return redirect('/listacontratista')
    
    else:
        return redirect('/listacontratista')

# Vista para eliminar un Contratista
def eliminarcontratista(request, contratista_id):
    contratistaEliminar = Contratista.objects.get(id=contratista_id)
    contratistaEliminar.delete()
    messages.success(request, "Contratista Eliminado Exitosamente")
    return redirect('/listacontratista')

# Vista para editar un Contratista
def editarcontratista(request, contratista_id):
    contratistaEditar = Contratista.objects.get(id=contratista_id)
    return render(request, 'editarcontratista.html', {'contratista': contratistaEditar})

# Vista para procesar la edición de un Contratista
def procesarEdicioncontratista(request):
    contratista = Contratista.objects.get(id=request.POST['id'])
    contratista.nombre = request.POST['nombre']
    contratista.email = request.POST['email']
    contratista.telefono = request.POST['telefono']

    contratista.save()
    messages.success(request, "Contratista Actualizado Exitosamente")
    return redirect('/listacontratista')

# Oficina -------------------------------------------------------------------------------------------------

# Vista para mostrar el formulario de nueva Oficina
def nuevaoficina(request):
    return render(request, 'nuevaoficina.html')

# Vista para mostrar la lista de Oficinas
def listaoficina(request):
    oficinas = Oficina.objects.all()
    return render(request, 'listaoficina.html', {'oficinas': oficinas})

# Vista para guardar una nueva Oficina
def guardaroficina(request):
    nombre = request.POST['nombre']
    direccion = request.POST['direccion']
    capacidad = request.POST['capacidad']
    foto = request.FILES.get('foto', None)

    
    # Crear la nueva oficina
    Oficina.objects.create(
        nombre=nombre,
        direccion=direccion,
        capacidad=capacidad,
        foto=foto
    )
    
    messages.success(request, "Oficina Guardada Exitosamente")
    return redirect('/listaoficina')

# Vista para eliminar una Oficina
def eliminaroficina(request, oficina_id):
    oficinaEliminar = Oficina.objects.get(id=oficina_id)
    oficinaEliminar.delete()
    messages.success(request, "Oficina Eliminada Exitosamente")
    return redirect('/listaoficina')

# Vista para editar una Oficina
def editaroficina(request, oficina_id):
    oficinaEditar = Oficina.objects.get(id=oficina_id)
    return render(request, 'editaroficina.html', {'oficina': oficinaEditar})

# Vista para procesar la edición de una Oficina
def procesarEdicionoficina(request):
    oficina = get_object_or_404(Oficina, id=request.POST.get('id'))

    # Actualizar los campos del formulario
    oficina.nombre = request.POST.get('nombre', oficina.nombre)
    oficina.direccion = request.POST.get('direccion', oficina.direccion)
    oficina.capacidad = request.POST.get('capacidad', oficina.capacidad)

    # Manejo seguro de la foto
    if 'foto' in request.FILES:  
        oficina.foto = request.FILES['foto']  

    oficina.save()
    messages.success(request, "Oficina Actualizada Exitosamente")
    return redirect('/listaoficina')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Reforma, Oficina, Contratista, Suministro

# Vista para mostrar el formulario de nueva Reforma
def nuevareforma(request):
    oficinas = Oficina.objects.all()
    contratistas = Contratista.objects.all()
    suministros = Suministro.objects.all()
    return render(request, 'nuevareforma.html', {
        'oficinas': oficinas,
        'contratistas': contratistas,
        'suministros': suministros
    })

# Vista para mostrar la lista de Reformas
def listareforma(request):
    reformas = Reforma.objects.all()
    return render(request, 'listareforma.html', {'reformas': reformas})

# Vista para guardar una nueva Reforma
def guardarreforma(request):
    if request.method == "POST":
        oficina = get_object_or_404(Oficina, id=request.POST['oficina'])
        contratista = get_object_or_404(Contratista, id=request.POST['contratista'])
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        presupuesto = request.POST['presupuesto']
        suministros = request.POST.getlist('suministros')  # Obtiene una lista de IDs
        observacion = request.POST.get('observacion', '')
        evidencia = request.FILES.get('evidencia')  # Archivos deben manejarse con request.FILES
        email = request.POST['email']
        telefono = request.POST['telefono']
        finalizado = request.POST.get('finalizado', False) == 'on'  # Convierte en Booleano

        # Crear la nueva reforma
        reforma = Reforma.objects.create(
            oficina=oficina,
            contratista=contratista,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            presupuesto=presupuesto,
            observacion=observacion,
            evidencia=evidencia,
            email=email,
            telefono=telefono,
            finalizado=finalizado
        )
        # Crear el mensaje de correo
        subject = 'Confirmación trabajos'
        message = f'Hola le saluda la empresa {oficina} tu {contratista},\n\nHemos recibido que tu puedes trabajor y le pagaremos :\n\n{presupuesto}\n\n y si esta a gusto comuniquenos    .................Gracias por comunicarte con nosotros.'
        from_email = 'no-reply@miweb.com'  # Dirección de correo que enviará el mensaje
        recipient_list = [email]  # Correo del usuario que ingresó

        # Crear el objeto EmailMessage
        email_message = EmailMessage(
            subject,
            message,
            from_email,
            recipient_list,
        )

        # Adjuntar el archivo si existe evidencia
        if evidencia:
            email_message.attach(evidencia.name, evidencia.read(), evidencia.content_type)

        # Enviar el correo
        email_message.send(fail_silently=False)

        # Agregar mensaje de éxito
        messages.success(request, "reformas Guardada Exitosamente")

        # Redirigir a la página de listado de quejas
        return redirect('/listareforma')


# Vista para eliminar una Reforma
def eliminarreforma(request, reforma_id):
    reforma = get_object_or_404(Reforma, id=reforma_id)
    reforma.delete()
    messages.success(request, "Reforma eliminada exitosamente")
    return redirect('/listareforma')

# Vista para editar una Reforma
def editarreforma(request, reforma_id):
    reforma = get_object_or_404(Reforma, id=reforma_id)
    oficinas = Oficina.objects.all()
    contratistas = Contratista.objects.all()
    suministros = Suministro.objects.all()

    return render(request, 'editarreforma.html', {
        'reforma': reforma,
        'oficinas': oficinas,
        'contratistas': contratistas,
        'suministros': suministros
    })

# Vista para procesar la edición de una Reforma
def procesarEdicionreforma(request):
    if request.method == "POST":
        reforma = get_object_or_404(Reforma, id=request.POST['id'])

        reforma.oficina = get_object_or_404(Oficina, id=request.POST['oficina'])
        reforma.contratista = get_object_or_404(Contratista, id=request.POST['contratista'])
        reforma.fecha_inicio = request.POST['fecha_inicio']
        reforma.fecha_fin = request.POST['fecha_fin']
        reforma.presupuesto = request.POST['presupuesto']
        reforma.observacion = request.POST.get('observacion', '')
        reforma.email = request.POST['email']
        reforma.telefono = request.POST['telefono']
        reforma.finalizado = request.POST.get('finalizado', False) == 'on'

        # Actualizar suministros
        suministros = request.POST.getlist('suministros')
        reforma.suministros.set(Suministro.objects.filter(id__in=suministros))

        # Si hay nueva evidencia, reemplazarla
        if 'evidencia' in request.FILES:
            reforma.evidencia = request.FILES['evidencia']

        reforma.save()
        messages.success(request, "Reforma actualizada exitosamente")
        return redirect('/listareforma')


# Suministro -------------------------------------------------------------------------------------------------

# Vista para mostrar el formulario de nuevo Suministro
def nuevasuministro(request):
    return render(request, 'nuevasuministro.html')

# Vista para mostrar la lista de Suministros
def listasuministro(request):
    suministros = Suministro.objects.all()
    return render(request, 'listasuministro.html', {'suministros': suministros})

# Vista para guardar un nuevo Suministro
def guardarsuministro(request):
    nombre = request.POST['nombre']
    descripcion = request.POST.get('descripcion', '')  # Usa `.get()` para evitar errores

    costo = request.POST['costo']
    evidencia = request.FILES.get('evidencia', None)

    
    # Crear el nuevo suministro
    Suministro.objects.create(
        nombre=nombre,
        descripcion =descripcion,
        costo=costo,
        evidencia=evidencia

    )
    
    messages.success(request, "Suministro Guardado Exitosamente")
    return redirect('/listasuministro')

# Vista para eliminar un Suministro
def eliminarsuministro(request, suministro_id):
    suministroEliminar = Suministro.objects.get(id=suministro_id)
    suministroEliminar.delete()
    messages.success(request, "Suministro Eliminado Exitosamente")
    return redirect('/listasuministro')

# Vista para editar un Suministro
def editarsuministro(request, suministro_id):
    suministroEditar = Suministro.objects.get(id=suministro_id)
    return render(request, 'editarsuministro.html', {'suministro': suministroEditar})

# Vista para procesar la edición de un Suministro
def procesarEdicionsuministro(request):
    # Obtener el suministro con el id recibido
    suministro = Suministro.objects.get(id=request.POST['id'])
    
    # Actualizar los campos del suministro con los datos del formulario
    suministro.nombre = request.POST.get('nombre', '')  # Usar .get() para evitar errores
    suministro.descripcion = request.POST.get('descripcion', '')  # Usar .get()
    suministro.costo = request.POST.get('costo', '')  # Usar .get()
    
    # Para el campo 'evidencia', asegurémonos de que se maneje correctamente
    suministro.evidencia = request.FILES.get('evidencia')  # Si 'evidencia' es un archivo

    # Guardar los cambios en la base de datos
    suministro.save()
    
    # Mostrar un mensaje de éxito
    messages.success(request, "Suministro Actualizado Exitosamente")
    
    # Redirigir a la lista de suministros
    return redirect('/listasuministro')

def exportar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

    p = canvas.Canvas(response, pagesize=letter)

    def encabezado():
        """Dibuja el encabezado en cada página."""
        p.setFont("Helvetica-Bold", 14)
        p.drawString(150, 750, "Contratistas, Oficinas, Reformas y Suministros")
        p.line(50, 745, 550, 745)  # Línea divisoria
        return 730  # Posición Y inicial

    def nueva_pagina():
        """Crea una nueva página y devuelve la posición Y inicial."""
        p.showPage()
        return encabezado()

    # Dibujar encabezado inicial
    y_position = encabezado()
    p.setFont("Helvetica", 10)

    def agregar_seccion(titulo, datos):
        """Agrega una sección al PDF con su título y datos."""
        nonlocal y_position
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_position, titulo)
        y_position -= 15
        p.setFont("Helvetica", 10)

        if not datos:
            p.drawString(50, y_position, "No hay datos disponibles.")
            y_position -= 20

        for linea in datos:
            wrapped_text = simpleSplit(linea, "Helvetica", 10, 450)
            for text in wrapped_text:
                p.drawString(60, y_position, text)
                y_position -= 15
                if y_position < 100:
                    y_position = nueva_pagina()

            y_position -= 10  # Espaciado entre elementos

    # **Contratistas**
    contratistas = Contratista.objects.all()
    datos_contratistas = [f"{c.nombre} - Teléfono: {c.telefono} - Email: {c.email}" for c in contratistas]
    agregar_seccion("Contratistas:", datos_contratistas)

    # **Oficinas**
    oficinas = Oficina.objects.all()
    datos_oficinas = [f"{o.nombre} - Dirección: {o.direccion} - Capacidad: {o.capacidad}" for o in oficinas]
    agregar_seccion("Oficinas:", datos_oficinas)

    # **Reformas**
    reformas = Reforma.objects.all()
    datos_reformas = [
        f"Reforma en {r.oficina.nombre} - Contratista: {r.contratista.nombre} - Inicio: {r.fecha_inicio} - "
        f"Fin: {r.fecha_fin} - Presupuesto: ${r.presupuesto}" for r in reformas
    ]
    agregar_seccion("Reformas:", datos_reformas)

    # **Suministros**
    suministros = Suministro.objects.all()
    datos_suministros = [f"{s.nombre} - {s.descripcion} - Costo: ${s.costo}" for s in suministros]
    agregar_seccion("Suministros:", datos_suministros)

    p.showPage()
    p.save()
    
    return response