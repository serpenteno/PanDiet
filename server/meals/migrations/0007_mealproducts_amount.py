# Generated by Django 5.1.4 on 2024-12-17 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0006_meal_tags_alter_meal_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='mealproducts',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=5),
            preserve_default=False,
        ),
    ]
