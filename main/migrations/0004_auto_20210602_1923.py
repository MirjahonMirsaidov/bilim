# Generated by Django 3.1.2 on 2021-06-02 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210601_1215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionimage',
            old_name='images',
            new_name='image',
        ),
    ]