# Generated by Django 2.2.4 on 2020-01-23 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0013_recommendedbeer_percent_match'),
        ('users', '0009_auto_20181018_0112'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BeerPreferences',
            new_name='BeerProfile',
        ),
        migrations.AlterModelTable(
            name='beerprofile',
            table='users_beerpreferences',
        ),
    ]
