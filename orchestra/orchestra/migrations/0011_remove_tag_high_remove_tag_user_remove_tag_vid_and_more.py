# Generated by Django 5.0 on 2024-09-25 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orchestra', '0010_alter_vid_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='high',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='user',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='vid',
        ),
        migrations.CreateModel(
            name='TagMapper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('high', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tagMappers', to='orchestra.high')),
                ('tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tagMapper', to='orchestra.tag')),
                ('vid', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tagMappers', to='orchestra.vid')),
            ],
            options={
                'verbose_name': 'tagMapper',
                'verbose_name_plural': 'tagMapper',
            },
        ),
    ]
