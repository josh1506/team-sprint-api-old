# Generated by Django 4.0.10 on 2023-03-15 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        ('sprint', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project.project'),
            preserve_default=False,
        ),
    ]