from django.db import models

# Create your models here.


class Pokemon(models.Model):
    name = models.CharField(max_length=500)
    front_image = models.URLField(blank=True, null=True)
