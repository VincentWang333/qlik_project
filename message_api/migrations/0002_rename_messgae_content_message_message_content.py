# Generated by Django 3.2.11 on 2022-01-16 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='messgae_content',
            new_name='message_content',
        ),
    ]
