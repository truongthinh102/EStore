# Generated by Django 4.0 on 2022-10-20 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_khachhang_dia_chi_alter_khachhang_dien_thoai_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='khachhang',
            name='dia_chi',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='khachhang',
            name='dien_thoai',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='khachhang',
            name='ho',
            field=models.CharField(max_length=264),
        ),
        migrations.AlterField(
            model_name='khachhang',
            name='mat_khau',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='khachhang',
            name='ten',
            field=models.CharField(max_length=264),
        ),
    ]
