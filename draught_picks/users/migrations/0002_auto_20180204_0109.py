# Generated by Django 2.0.1 on 2018-02-04 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draughtpicksuser',
            name='date_of_birth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='draughtpicksuser',
            name='weight',
            field=models.IntegerField(blank=True, help_text='Weight in pounds.', null=True),
        ),
    ]