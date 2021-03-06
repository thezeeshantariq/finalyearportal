# Generated by Django 2.1.2 on 2018-10-06 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20181006_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentnotifications',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentnotifications',
            name='is_viewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='studentnotifications',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='app.Student'),
        ),
        migrations.AlterField(
            model_name='studentnotifications',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='app.Student'),
        ),
    ]
