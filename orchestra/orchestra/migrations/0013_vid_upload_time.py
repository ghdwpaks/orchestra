# Generated by Django 5.0 on 2024-09-26 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orchestra', '0012_alter_tagmapper_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='vid',
            name='upload_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
