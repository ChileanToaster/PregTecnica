from django.db import models

class Activo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Activo'
        verbose_name_plural = 'Activos'

class PrecioActivo(models.Model):
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE, related_name='precios')
    fecha = models.DateField()
    precio = models.DecimalField(max_digits=10, decimal_places=6)

    def __str__(self):
        return f"{self.activo.nombre} - {self.fecha} - {self.precio}"

    class Meta:
        verbose_name = 'Precio de Activo'
        verbose_name_plural = 'Precios de Activos'
        ordering = ['fecha']