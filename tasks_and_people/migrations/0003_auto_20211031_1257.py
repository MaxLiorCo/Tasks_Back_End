# Generated by Django 3.2.8 on 2021-10-31 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_and_people', '0002_task_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='task',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
