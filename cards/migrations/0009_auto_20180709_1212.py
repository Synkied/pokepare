# Generated by Django 2.0.6 on 2018-07-09 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0008_auto_20180709_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='hp',
            field=models.CharField(blank=True, help_text='The number of the card for the set it was released in. Found on the bottom right side of the card.', max_length=10, null=True),
        ),
    ]
