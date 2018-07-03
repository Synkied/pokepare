from django.db import models
from django.utils import timezone
from django.conf import settings

from pokemons.models import Pokemon

# Create your models here.


class Card(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=255, blank=True, null=True)
    card_type = models.CharField(max_length=50, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    number = models.CharField(max_length=20, blank=True, null=True)
    card_set = models.CharField(max_length=255, blank=True, null=True)
    condition = models.CharField(max_length=50, blank=True, null=True)
    edition = models.CharField(max_length=255, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    language = models.CharField(max_length=5, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    image = models.URLField(default=settings.CARD_PLACEHOLDER)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created_at',)
