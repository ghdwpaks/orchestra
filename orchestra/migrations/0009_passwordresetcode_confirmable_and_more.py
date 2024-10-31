# Generated by Django 5.0 on 2024-09-18 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orchestra', '0008_passwordresetcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordresetcode',
            name='confirmable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='passwordresetcode',
            name='useable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='uid',
            field=models.CharField(default=None, max_length=50),
        ),
    ]