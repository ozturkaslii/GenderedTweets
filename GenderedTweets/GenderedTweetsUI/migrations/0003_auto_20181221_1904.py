# Generated by Django 2.1.4 on 2018-12-21 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GenderedTweetsUI', '0002_auto_20181218_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='text',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
