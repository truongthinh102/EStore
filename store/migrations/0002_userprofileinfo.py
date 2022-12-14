# Generated by Django 4.0 on 2022-10-13 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolio', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(default='users/no-avatar.png', upload_to='users/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='auth.user')),
            ],
            options={
                'db_table': 'user_profile_info',
            },
        ),
    ]
