# Generated by Django 3.2.8 on 2021-10-31 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_and_people', '0003_auto_20211031_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='activeTaskCount',
            field=models.IntegerField(default=0),
        ),
    ]