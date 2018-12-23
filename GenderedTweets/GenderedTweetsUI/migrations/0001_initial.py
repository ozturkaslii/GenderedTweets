# Generated by Django 2.1.4 on 2018-12-17 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tweet_id_str', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('text', models.DateField(blank=True, max_length=300, null=True)),
                ('user_id_str', models.CharField(blank=True, max_length=250, null=True)),
                ('user_name', models.CharField(blank=True, max_length=150, null=True)),
                ('user_screen_name', models.CharField(blank=True, max_length=150, null=True)),
                ('user_location', models.CharField(blank=True, max_length=150, null=True)),
                ('quote_count', models.IntegerField(blank=True, default=0, null=True)),
                ('reply_count', models.IntegerField(blank=True, default=0, null=True)),
                ('retweet_count', models.IntegerField(blank=True, default=0, null=True)),
                ('favorite_count', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]
