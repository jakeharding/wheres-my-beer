# Generated by Django 2.0.1 on 2018-03-13 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0006_auto_20180312_0301'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeerLearning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('malt', models.IntegerField(default=0)),
                ('hops', models.IntegerField(default=0)),
                ('india', models.IntegerField(default=0)),
                ('america', models.IntegerField(default=0)),
                ('german', models.IntegerField(default=0)),
                ('belgium', models.IntegerField(default=0)),
                ('ireland', models.IntegerField(default=0)),
                ('europe', models.IntegerField(default=0)),
                ('bohemian', models.IntegerField(default=0)),
                ('baltic', models.IntegerField(default=0)),
                ('coffee', models.IntegerField(default=0)),
                ('chocolate', models.IntegerField(default=0)),
                ('caramel', models.IntegerField(default=0)),
                ('wheat', models.IntegerField(default=0)),
                ('vanilla', models.IntegerField(default=0)),
                ('strawberry', models.IntegerField(default=0)),
                ('almond', models.IntegerField(default=0)),
                ('coconut', models.IntegerField(default=0)),
                ('pineapple', models.IntegerField(default=0)),
                ('plum', models.IntegerField(default=0)),
                ('mango', models.IntegerField(default=0)),
                ('orange', models.IntegerField(default=0)),
                ('peach', models.IntegerField(default=0)),
                ('toffee', models.IntegerField(default=0)),
                ('honey', models.IntegerField(default=0)),
                ('hazelnut', models.IntegerField(default=0)),
                ('blueberry', models.IntegerField(default=0)),
                ('banana', models.IntegerField(default=0)),
                ('pumpkin', models.IntegerField(default=0)),
                ('tart', models.IntegerField(default=0)),
                ('sour', models.IntegerField(default=0)),
                ('sweet', models.IntegerField(default=0)),
                ('dry', models.IntegerField(default=0)),
                ('oats', models.IntegerField(default=0)),
                ('light_colors', models.IntegerField(default=0)),
                ('dark_colors', models.IntegerField(default=0)),
                ('bitter', models.IntegerField(default=0)),
                ('lambic', models.IntegerField(default=0)),
                ('lager', models.IntegerField(default=0)),
                ('porter', models.IntegerField(default=0)),
                ('stouts', models.IntegerField(default=0)),
                ('ales', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='beer',
            name='beer_learning',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='beer', to='beers.BeerLearning'),
        ),
    ]
