# Generated by Django 5.0.3 on 2024-03-14 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_customuser_options_customuser_email_verified'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Person', 'verbose_name_plural': 'People'},
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='email_verified',
        ),
    ]