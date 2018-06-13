from django.db import models

# Create your models here.


class Card(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=255)
    card_type = models.CharField(max_length=50)
    version = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    card_set = models.CharField(max_length=255)
    condition = models.CharField(max_length=50)
    edition = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    language = models.CharField(max_length=5)
    url = models.URLField()
