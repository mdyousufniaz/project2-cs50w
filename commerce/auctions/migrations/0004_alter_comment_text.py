# Generated by Django 5.0.6 on 2024-07-04 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_bid_listing_alter_comment_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=500),
        ),
    ]
