# Generated by Django 3.2.9 on 2022-06-06 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0002_auto_20220525_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='answermodel',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='users.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resultmodel',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='result', to='users.user'),
            preserve_default=False,
        ),
    ]
