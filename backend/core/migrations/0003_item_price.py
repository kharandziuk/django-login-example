# Generated by Django 2.2.1 on 2021-01-21 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_auto_20210120_2131"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="price",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]