# Generated by Django 3.2.5 on 2021-10-02 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dadova', '0006_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='courses',
            field=models.ManyToManyField(blank=None, to='dadova.Review'),
        ),
    ]