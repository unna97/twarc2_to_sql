# Generated by Django 4.0.6 on 2022-07-26 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0007_alter_replied_in_reply_to_user_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="replied",
            old_name="in_reply_to_user_id",
            new_name="in_reply_to_user",
        ),
    ]
