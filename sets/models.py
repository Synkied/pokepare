from django.db import models
from django.utils import timezone
from utils import OverwriteStorage

# Create your models here.


class Set(models.Model):
    name = models.CharField(
        help_text='The set name.',
        max_length=500,
    )
    code = models.CharField(
        help_text='The code name of the set.',
        max_length=50,
    )
    series = models.CharField(
        help_text='The series the set belongs to.',
        max_length=50,
        blank=True,
        null=True,
    )
    release_date = models.CharField(
        help_text='The date the set was released.',
        max_length=20,
        blank=True,
        null=True,
    )
    total_cards = models.PositiveIntegerField(blank=True, null=True)
    symbol_url = models.URLField(blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    image = models.ImageField(storage=OverwriteStorage(), upload_to="sets/logos/", blank=True, null=True)

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created_at',)
