# Generated by Django 5.1.2 on 2025-02-18 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0002_usuario_groups_usuario_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='tutorial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Tutoriales_cursos', to='tutorial.tutorial'),
        ),
    ]
