# Generated by Django 5.0 on 2024-09-23 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orchestra', '0009_passwordresetcode_confirmable_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vid',
            name='name',
            field=models.CharField(blank=True, max_length=127),
        ),
    ]