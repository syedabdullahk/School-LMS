# Generated by Django 3.2.9 on 2022-04-14 21:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_name', models.CharField(max_length=200)),
                ('assignment_description', models.TextField()),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('due_date', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubmitAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('assignment_file', models.FileField(upload_to='')),
                ('submitted_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('assignment_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignment.assignment')),
            ],
        ),
    ]
