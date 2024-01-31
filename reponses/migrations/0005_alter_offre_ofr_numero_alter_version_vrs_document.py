# Generated by Django 4.2.3 on 2023-08-11 07:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reponses', '0004_alter_offre_ofr_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offre',
            name='Ofr_numero',
            field=models.CharField(max_length=16, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(8)]),
        ),
        migrations.AlterField(
            model_name='version',
            name='Vrs_document',
            field=models.ImageField(blank=True, null=True, upload_to='Documents/Contrat'),
        ),
    ]
