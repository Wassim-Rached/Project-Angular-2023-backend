# Generated by Django 4.2.6 on 2023-11-22 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_joinclubform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joinclubform',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='pending', max_length=8),
        ),
    ]