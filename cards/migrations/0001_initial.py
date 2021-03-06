# Generated by Django 2.0.6 on 2018-07-05 11:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pokemons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('card_type', models.CharField(blank=True, max_length=50, null=True)),
                ('version', models.CharField(blank=True, help_text='Regular/Foil...', max_length=50, null=True)),
                ('number', models.CharField(blank=True, max_length=20, null=True)),
                ('card_set', models.CharField(blank=True, max_length=255, null=True)),
                ('series', models.CharField(blank=True, max_length=255, null=True)),
                ('year', models.PositiveIntegerField(blank=True, null=True)),
                ('language', models.CharField(blank=True, max_length=5, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('image', models.URLField(default='/static/img/pokepare_card.png')),
                ('condition', models.CharField(blank=True, max_length=50, null=True)),
                ('edition', models.CharField(blank=True, max_length=50, null=True)),
                ('rarity', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('pokemon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='pokemons.Pokemon')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
    ]
