# Generated by Django 4.2.6 on 2023-10-27 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_rename_activitylikes_activitylike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
