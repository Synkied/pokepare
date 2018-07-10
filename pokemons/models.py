from django.db import models

# Create your models here.


class Pokemon(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to="pokemons/", blank=True, null=True)
    number = models.PositiveIntegerField()
