# Generated by Django 3.1.2 on 2020-10-20 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20201020_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(verbose_name='Score')),
                ('finished', models.DateField(verbose_name='Finished')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.game')),
            ],
        ),
        migrations.CreateModel(
            name='GameType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
            ],
        ),
        migrations.DeleteModel(
            name='UserList',
        ),
        migrations.AddField(
            model_name='gamelist',
            name='game_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.gametype'),
        ),
        migrations.AddField(
            model_name='gamelist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
