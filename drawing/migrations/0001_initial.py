# Generated by Django 4.2.1 on 2023-05-25 04:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Drawing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='주문일')),
                ('modifeid_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('link', models.URLField()),
                ('status', models.CharField(choices=[('active', '활성'), ('inactive', '비활성')], default='active', max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Animation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='주문일')),
                ('modifeid_at', models.DateTimeField(auto_now=True, null=True)),
                ('link', models.URLField()),
                ('purpose', models.CharField(choices=[('wait1', '대기1'), ('wait2', '대기2'), ('listen1', '듣는중1'), ('listen2', '듣는중2')], max_length=10)),
                ('drawing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drawing.drawing')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]