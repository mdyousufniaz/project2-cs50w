# Generated by Django 5.0.6 on 2024-07-09 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_comment_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='observers', to='auctions.listing'),
        ),
    ]
