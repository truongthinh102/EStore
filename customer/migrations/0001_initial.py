# Generated by Django 4.0 on 2022-10-20 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KhachHang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ho', models.CharField(max_length=264)),
                ('ten', models.CharField(max_length=264)),
                ('email', models.EmailField(max_length=254)),
                ('mat_khau', models.CharField(max_length=50)),
                ('dien_thoai', models.CharField(max_length=20)),
                ('dia_chi', models.TextField()),
            ],
        ),
    ]
