# Generated by Django 4.2.3 on 2023-08-11 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reponses', '0003_alter_offre_ofr_document_alter_paiement_pmt_document_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offre',
            name='Ofr_document',
            field=models.ImageField(upload_to='Documents/Offre/'),
        ),
    ]
