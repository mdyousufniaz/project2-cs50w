# Generated by Django 5.0.6 on 2024-07-10 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_user_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='user',
            new_name='bidder',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='commenter',
        ),
    ]
