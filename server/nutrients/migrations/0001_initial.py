# Generated by Django 5.1.3 on 2024-12-05 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nutrient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('unit', models.CharField(choices=[('g', 'Gram'), ('mg', 'Milligram'), ('mcg', 'Microgram'), ('kg', 'Kilogram'), ('ml', 'Milliliter'), ('l', 'Liter')], max_length=10)),
            ],
        ),
    ]
