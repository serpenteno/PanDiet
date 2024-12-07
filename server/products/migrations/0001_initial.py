# Generated by Django 5.1.3 on 2024-12-05 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nutrients', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('mass', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tags', models.IntegerField(choices=[(1, 'Salt'), (2, 'Sugar'), (4, 'Fat'), (8, 'Processed Food'), (16, 'Additives'), (32, 'Gluten'), (64, 'Milk'), (128, 'Eggs'), (256, 'Nuts'), (512, 'Peanuts'), (1024, 'Sesame'), (2048, 'Soybeans'), (4096, 'Celery'), (8192, 'Mustard'), (16384, 'Lupin'), (32768, 'Fish'), (65536, 'Crustaceans'), (131072, 'Molluscs'), (262144, 'Vegan'), (524288, 'Vegetarian'), (1048576, 'Palm Oil')], default=0)),
                ('visibility', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], max_length=10)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='ProductNutrients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nutrient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutrients.nutrient')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='nutrients',
            field=models.ManyToManyField(through='products.ProductNutrients', to='nutrients.nutrient'),
        ),
    ]
