# Generated by Django 2.2.16 on 2021-09-16 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20210916_1613'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-pub_date', '-pk']},
        ),
    ]
