# Generated by Django 3.1.2 on 2021-05-05 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_contabilidad_inversiones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plataformas_inversion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_plataforma', models.CharField(max_length=12)),
            ],
        ),
        migrations.AlterField(
            model_name='transacciones',
            name='plataforma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plataformas', to='app_contabilidad_inversiones.plataformas_inversion'),
        ),
    ]
