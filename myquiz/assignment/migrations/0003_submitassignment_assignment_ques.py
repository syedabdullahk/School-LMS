# Generated by Django 3.2.9 on 2022-04-15 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0002_alter_submitassignment_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='submitassignment',
            name='assignment_ques',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question', to='assignment.assignment'),
        ),
    ]
