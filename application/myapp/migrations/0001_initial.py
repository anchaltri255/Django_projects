# Generated by Django 5.0.4 on 2024-11-01 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittle', models.CharField(max_length=100)),
                ('selling_price', models.FloatField()),
                ('discounted_price', models.FloatField()),
                ('description', models.TextField()),
                ('composition', models.TextField(default='')),
                ('prodapp', models.TextField(default='')),
                ('category', models.CharField(choices=[('CH', 'Chair'), ('CO', 'Cooler'), ('TB', 'Table'), ('FG', 'Fridge'), ('TB', 'Table2'), ('DR', 'Dressing'), ('FUN', 'Furniture'), ('BED', 'Bed')], max_length=10)),
                ('product_image', models.ImageField(upload_to='product')),
            ],
        ),
    ]