# Generated by Django 5.1.3 on 2025-01-10 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_tags'),
        ('tags', '0002_tag_inheritance_and_logic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, to='tags.tag'),
        ),
    ]
