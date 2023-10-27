# Generated by Django 4.2.6 on 2023-10-27 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_account_photo'),
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='accounts_registrations',
            field=models.ManyToManyField(blank=True, related_name='activities_registrations', through='activities.ActivityRegistration', to='accounts.account'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='activities', through='activities.ActivityCategory', to='activities.category'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_activites', through='activities.ActivityLikes', to='accounts.account'),
        ),
    ]