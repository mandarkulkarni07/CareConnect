# Generated by Django 4.0.4 on 2022-05-05 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='Time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
