# Generated by Django 2.0.6 on 2018-07-10 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0012_card_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='prices',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
