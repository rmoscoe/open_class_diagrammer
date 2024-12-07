# Generated by Django 5.1.2 on 2024-11-20 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class_manager', '0006_alter_module_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='relationships',
            field=models.ManyToManyField(blank=True, help_text='Related class(es).', null=True, through='class_manager.Relationship', to='class_manager.class'),
        ),
    ]
