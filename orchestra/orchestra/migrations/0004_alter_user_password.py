# Generated by Django 5.0 on 2024-09-02 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orchestra', '0003_alter_user_managers_remove_user_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
