# Generated by Django 5.0 on 2024-09-25 08:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orchestra', '0011_remove_tag_high_remove_tag_user_remove_tag_vid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagmapper',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tagMappers', to='orchestra.tag'),
        ),
    ]
