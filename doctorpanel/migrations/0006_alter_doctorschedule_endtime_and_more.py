# Generated by Django 4.0.4 on 2022-05-05 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctorpanel', '0005_doctorschedule_lastime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorschedule',
            name='Endtime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctorschedule',
            name='Startime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctorschedule',
            name='averageconsultime',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctorschedule',
            name='lastime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
