# Generated by Django 3.2 on 2023-05-10 22:53

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20230507_0938'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='user',
            name='unique_username&email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[reviews.validators.validate_username], verbose_name='Имя пользователя'),
        ),
    ]
