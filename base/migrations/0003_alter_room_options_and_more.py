# Generated by Django 4.1.5 on 2023-01-23 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_message_topic_delete_user_room_host_alter_room_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated_at', '-created_at']},
        ),
        migrations.RenameField(
            model_name='room',
            old_name='decription',
            new_name='description',
        ),
    ]