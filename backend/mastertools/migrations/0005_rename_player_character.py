# Generated by Django 4.1.5 on 2023-01-23 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mastertools', '0004_npc'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Player',
            new_name='Character',
        ),
    ]
