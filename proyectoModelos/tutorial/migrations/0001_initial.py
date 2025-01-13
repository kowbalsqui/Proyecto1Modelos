# Generated by Django 5.1.2 on 2025-01-13 12:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nombre', models.CharField(max_length=30)),
                ('fecha_Registro', models.DateField()),
                ('puntuacion', models.DecimalField(decimal_places=1, max_digits=3)),
                ('es_activo', models.BooleanField(default=True)),
                ('es_staff', models.BooleanField(default=False)),
                ('es_superuser', models.BooleanField(default=False)),
                ('rol', models.PositiveSmallIntegerField(choices=[(1, 'administrador'), (2, 'profesor'), (3, 'estudiante')], default=1)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='imagenes/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('es_activa', models.BooleanField(default=False)),
                ('popularidad', models.DecimalField(decimal_places=1, max_digits=3)),
                ('descripcion', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('publica', models.BooleanField(default=False)),
                ('descripcion', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_Guardado', models.DateTimeField(auto_now=True)),
                ('comentario_Destacado', models.TextField(max_length=300)),
                ('importancia', models.DecimalField(decimal_places=1, max_digits=3)),
                ('notificacion', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField(max_length=300)),
                ('fecha', models.DateTimeField()),
                ('visible', models.BooleanField(default=False)),
                ('puntuacion', models.DecimalField(decimal_places=1, max_digits=3)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Comentarios_de_Usuarios', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=300)),
                ('horas', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('usuario', models.ManyToManyField(related_name='usuarios_del_curso', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Certificado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_emision', models.DateField()),
                ('codigo_verificacion', models.CharField(max_length=50)),
                ('nivel', models.IntegerField()),
                ('url_descarga', models.CharField(max_length=50)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Certificado_Usuarios', to=settings.AUTH_USER_MODEL)),
                ('curso', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='certificado_Curso', to='tutorial.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Favorito_usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_favorito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorial.favorito')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='favorito',
            name='usuario',
            field=models.ManyToManyField(related_name='Favoritos_del_usuario', through='tutorial.Favorito_usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('fecha_Nacimiento', models.DateField()),
                ('redes', models.CharField(choices=[('IG', 'Instagram'), ('FB', 'Facebook'), ('TW', 'Twitter'), ('LI', 'LinkedIn')], max_length=50)),
                ('estudios', models.TextField(max_length=100)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfiles_Usuarios', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=300)),
                ('fecha_Creacion', models.DateTimeField()),
                ('activa', models.BooleanField(default=False)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CategoriaSubcategoria', to='tutorial.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('contenido', models.TextField()),
                ('fecha_Creacion', models.DateTimeField()),
                ('visitas', models.IntegerField()),
                ('valoracion', models.DecimalField(decimal_places=1, max_digits=3)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_del_tutorial', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='favorito',
            name='tutorial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Tutoriales_favoritos', to='tutorial.tutorial'),
        ),
        migrations.CreateModel(
            name='Etiqueta_tutorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_etiqueta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorial.etiqueta')),
                ('id_tutorial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorial.tutorial')),
            ],
        ),
        migrations.AddField(
            model_name='etiqueta',
            name='tutorial',
            field=models.ManyToManyField(related_name='Etiquetas_del_tutorial', through='tutorial.Etiqueta_tutorial', to='tutorial.tutorial'),
        ),
        migrations.AddField(
            model_name='curso',
            name='tutorial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Tutoriales_cursos', to='tutorial.tutorial'),
        ),
        migrations.AddField(
            model_name='categoria',
            name='tutorial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categoria_del_tutorial', to='tutorial.tutorial'),
        ),
    ]
