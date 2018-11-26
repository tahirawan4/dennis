# Generated by Django 2.0.4 on 2018-11-14 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days_ago', models.IntegerField(default=0)),
                ('source', models.CharField(max_length=30)),
                ('event', models.ManyToManyField(blank=True, null=True, to='users.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
    ]
