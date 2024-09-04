# Generated by Django 5.0 on 2024-09-04 12:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orchestra', '0004_alter_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=128, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록시각')),
                ('useable', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userTokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]