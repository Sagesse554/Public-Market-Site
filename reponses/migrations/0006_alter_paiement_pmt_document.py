# Generated by Django 4.2.3 on 2023-08-11 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reponses', '0005_alter_offre_ofr_numero_alter_version_vrs_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paiement',
            name='Pmt_document',
            field=models.ImageField(blank=True, null=True, upload_to='Documents/Paiement'),
        ),
    ]
