# Generated by Django 5.1.2 on 2024-12-12 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='imagen',
            field=models.ImageField(default='imagenes/home.png', upload_to='imagenes/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='certificado',
            name='fecha_emision',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='subcategoria',
            name='fecha_Creacion',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='fecha_Creacion',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='fecha_Registro',
            field=models.DateField(),
        ),
    ]
