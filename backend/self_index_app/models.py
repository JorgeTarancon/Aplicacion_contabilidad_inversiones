from django.db import models

# Create your models here.
class Usuario(models.Model):
    patrimonio = models.FloatField(max_length=14)