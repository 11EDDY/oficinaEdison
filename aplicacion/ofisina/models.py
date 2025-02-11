from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.mail import send_mail

class Oficina(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    capacidad = models.IntegerField()
    foto = models.ImageField(
        upload_to='oficinas_fotos/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nombre

class Contratista(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Suministro(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    evidencia = models.FileField(
        upload_to='suministros/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx'])]
    )

    def __str__(self):
        return self.nombre

class Reforma(models.Model):
    oficina = models.ForeignKey(Oficina, on_delete=models.CASCADE)
    contratista = models.ForeignKey(Contratista, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2)
    suministros = models.ManyToManyField(Suministro)
    observacion = models.TextField(null=True, blank=True)
    evidencia = models.FileField(
        upload_to='reformas/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx'])]
    )
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return f"Reforma de {self.oficina.nombre} - {self.fecha_inicio} a {self.fecha_fin}"

    class Meta:
        ordering = ['fecha_inicio', 'oficina']

    def save(self, *args, **kwargs):
        super(Reforma, self).save(*args, **kwargs)
        if self.finalizado:
            self.enviar_correo()

    def enviar_correo(self):
        subject = f"Finalización de reforma en {self.oficina.nombre}"
        message = f"La reforma en {self.oficina.nombre} ha finalizado. Fecha de finalización: {self.fecha_fin}."
        from_email = 'tucorreo@gmail.com'
        recipient_list = [self.email]
        send_mail(subject, message, from_email, recipient_list)
