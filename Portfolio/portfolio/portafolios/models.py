from django.db import models

class Portafolio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Portafolio'
        verbose_name_plural = 'Portafolios'

class ActivoPortafolio(models.Model):
    portafolio = models.ForeignKey(Portafolio, on_delete=models.CASCADE, related_name='activos')
    activo = models.ForeignKey('activos.Activo', on_delete=models.CASCADE, related_name='portafolios')
    cantidad = models.DecimalField(max_digits=18, decimal_places=5)

    def __str__(self):
        return f"{self.portafolio.nombre} - {self.activo.nombre} - {self.cantidad}"

    class Meta:
        verbose_name = 'Activo en Portafolio'
        verbose_name_plural = 'Activos en Portafolios'
        ordering = ['portafolio', 'activo']

        constraints = [
            models.UniqueConstraint(fields=['portafolio', 'activo'], name='unique_portafolio_activo'),
            models.CheckConstraint(check=models.Q(cantidad__gte=0), name='cantidad_positive_or_zero')
        ]