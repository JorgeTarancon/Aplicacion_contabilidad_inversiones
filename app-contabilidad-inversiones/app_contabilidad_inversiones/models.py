from django.db import models

# Create your models here.
class Plataformas_inversion(models.Model):
    nombre_plataforma = models.CharField(max_length=12)

    def __str__(self):
        return f"Nombre de la plataforma: {self.nombre_plataforma}"

class Transacciones(models.Model): # Cada clase de Python es una tabla de SQL
    fecha = models.DateField()
    nombre = models.CharField(max_length=250)
    plataforma = models.ForeignKey(Plataformas_inversion,on_delete=models.CASCADE, related_name="plataformas")

    precio = models.DecimalField(decimal_places=2,max_digits=6)

    def __str__(self):
        return f"{self.nombre}: con un precio de {self.precio} en la fecha {self.fecha}"