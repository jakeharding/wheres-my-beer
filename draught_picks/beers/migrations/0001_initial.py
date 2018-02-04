# Generated by Django 2.0.1 on 2018-02-04 00:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('abv', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('ibu', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('api_id', models.CharField(help_text='Unique id of the api the beer was pulled from', max_length=255)),
                ('name_of_api', models.CharField(help_text='Name of the api used to get data.', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BeerRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('rating', models.PositiveSmallIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('beer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='beers.Beer')),
            ],
        ),
    ]