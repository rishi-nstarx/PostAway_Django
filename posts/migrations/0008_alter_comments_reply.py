# Generated by Django 5.1 on 2024-08-27 07:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_alter_comments_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='reply',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_on_comments', to='posts.comments'),
        ),
    ]
