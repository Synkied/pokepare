from django.db import models

from utils import OverwriteStorage

# Create your models here.


class Pokemon(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(storage=OverwriteStorage(), upload_to="pokemons/", blank=True, null=True)
    number = models.PositiveIntegerField()
