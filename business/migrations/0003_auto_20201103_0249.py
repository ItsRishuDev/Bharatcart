# Generated by Django 3.1.2 on 2020-11-02 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_auto_20201028_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='business_mobile',
            field=models.BigIntegerField(),
        ),
    ]