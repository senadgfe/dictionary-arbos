# Generated by Django 4.2.2 on 2023-06-17 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_word_translation_alter_grammar_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='translation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
