# Generated by Django 4.1.2 on 2023-02-03 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='age',
            field=models.PositiveIntegerField(default=False),
            preserve_default=False,
        ),
    ]