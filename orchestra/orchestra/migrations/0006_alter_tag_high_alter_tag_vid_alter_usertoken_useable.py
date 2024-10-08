# Generated by Django 5.0 on 2024-09-07 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orchestra', '0005_usertoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='high',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='orchestra.high'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='vid',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='orchestra.vid'),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='useable',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
