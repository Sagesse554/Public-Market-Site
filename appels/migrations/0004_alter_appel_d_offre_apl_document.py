# Generated by Django 4.2.3 on 2023-08-08 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appels', '0003_alter_appel_a_manifestation_ami_document_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appel_d_offre',
            name='Apl_document',
            field=models.ImageField(blank=True, null=True, upload_to='Documents/AppeldOffre/'),
        ),
    ]