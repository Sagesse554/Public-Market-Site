# Generated by Django 4.2.3 on 2023-08-08 01:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allocation1',
            fields=[
                ('Alc1_id', models.AutoField(primary_key=True, serialize=False)),
                ('Prs_quantite', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Allocation2',
            fields=[
                ('Alc2_id', models.AutoField(primary_key=True, serialize=False)),
                ('Mtr_quantite', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('Ctg_id', models.AutoField(primary_key=True, serialize=False)),
                ('Ctg_titre', models.CharField(max_length=48)),
            ],
        ),
        migrations.CreateModel(
            name='Materiel',
            fields=[
                ('Mtr_id', models.AutoField(primary_key=True, serialize=False)),
                ('Mtr_titre', models.CharField(max_length=48)),
                ('Mtr_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('Prs_id', models.AutoField(primary_key=True, serialize=False)),
                ('Prs_titre', models.CharField(max_length=48)),
                ('Prs_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Prestation3',
            fields=[
                ('Ptn3_id', models.AutoField(primary_key=True, serialize=False)),
                ('Ptn3_description', models.TextField()),
                ('Ctg_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprises.categorie')),
            ],
        ),
        migrations.CreateModel(
            name='Registre',
            fields=[
                ('Rgs_numero', models.CharField(max_length=16, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message="Le numéro d'identification fiscale doit être au format valide.", regex='^\\d{8,16}$'), django.core.validators.MinLengthValidator(8)])),
                ('Rgs_denomination', models.CharField(max_length=64)),
                ('Rgs_dateCreation', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Entreprise',
            fields=[
                ('Ent_numero', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='entreprises.registre')),
                ('Ent_dateCreation', models.DateField()),
                ('Ent_evaluation', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('Rfc_id', models.AutoField(primary_key=True, serialize=False)),
                ('Rfc_titre', models.CharField(max_length=96)),
                ('Rfc_description', models.TextField()),
                ('Rfc_client', models.CharField(max_length=64)),
                ('Rfc_coordonnees', models.CharField(max_length=160)),
                ('Rfc_document', models.FileField(upload_to='media/Documents/Reference')),
                ('Rfc_typeContrat', models.CharField(max_length=48)),
                ('Rfc_dateDebut', models.DateField()),
                ('Rfc_dateFin', models.DateField()),
                ('Rfc_montant', models.FloatField()),
                ('Rfc_statut', models.CharField(choices=[('EN_COURS', 'En cours'), ('EN_ATTENTE', 'En attente'), ('TERMINEE', 'Terminée')], max_length=20)),
                ('Rfc_categories', models.ManyToManyField(through='entreprises.Prestation3', to='entreprises.categorie')),
                ('Ent_numero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprises.entreprise')),
            ],
        ),
        migrations.AddField(
            model_name='prestation3',
            name='Rfc_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprises.reference'),
        ),
        migrations.CreateModel(
            name='Prestation2',
            fields=[
                ('Ptn2_id', models.AutoField(primary_key=True, serialize=False)),
                ('Ptn2_description', models.TextField()),
                ('Ptn2_delai', models.IntegerField()),
                ('Ptn2_quantite', models.IntegerField()),
                ('Ptn2_tarif', models.FloatField()),
                ('Ctg_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprises.categorie')),
            ],
        ),
        migrations.CreateModel(
            name='Manifestation',
            fields=[
                ('Mnf_id', models.AutoField(primary_key=True, serialize=False)),
                ('Mnf_denomination', models.CharField(max_length=64)),
                ('Mnf_date', models.DateField(auto_now_add=True)),
                ('Mnf_logo', models.ImageField(blank=True, null=True, upload_to='media/Images/Logos/')),
                ('Mnf_adresse', models.CharField(max_length=96)),
                ('Mnf_telephone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message='Le numéro de téléphone doit être au format valide.', regex='^\\+?\\d{8,15}$')])),
                ('Mnf_email', models.EmailField(max_length=254)),
                ('Mnf_siteWeb', models.CharField(blank=True, max_length=48, null=True)),
                ('Mnf_document', models.FileField(upload_to='media/Documents/Manifestation/')),
                ('Ami_numero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appels.appel_a_manifestation')),
                ('Mnf_materiel', models.ManyToManyField(through='entreprises.Allocation2', to='entreprises.materiel')),
                ('Mnf_personnel', models.ManyToManyField(through='entreprises.Allocation1', to='entreprises.personnel')),
            ],
        ),
        migrations.AddField(
            model_name='allocation2',
            name='Mnf_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprises.manifestation'),
        ),
        migrations.AddField(
            model_name='allocation2',
            name='Mtr_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprises.materiel'),
        ),
        migrations.AddField(
            model_name='allocation2',
            name='Ptn2_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprises.prestation2'),
        ),
        migrations.AddField(
            model_name='allocation1',
            name='Mnf_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprises.manifestation'),
        ),
        migrations.AddField(
            model_name='allocation1',
            name='Prs_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprises.personnel'),
        ),
        migrations.AddField(
            model_name='allocation1',
            name='Ptn2_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprises.prestation2'),
        ),
        migrations.AddConstraint(
            model_name='prestation3',
            constraint=models.UniqueConstraint(fields=('Rfc_id', 'Ctg_id'), name='prestation3_pk'),
        ),
        migrations.AddField(
            model_name='manifestation',
            name='Ent_numero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprises.entreprise'),
        ),
        migrations.AddConstraint(
            model_name='allocation2',
            constraint=models.UniqueConstraint(fields=('Mnf_id', 'Ptn2_id', 'Mtr_id'), name='allocation2_pk'),
        ),
        migrations.AddConstraint(
            model_name='allocation1',
            constraint=models.UniqueConstraint(fields=('Mnf_id', 'Ptn2_id', 'Prs_id'), name='allocation1_pk'),
        ),
        migrations.AddConstraint(
            model_name='manifestation',
            constraint=models.UniqueConstraint(fields=('Ami_numero', 'Ent_numero'), name='manifestation_pk'),
        ),
    ]
