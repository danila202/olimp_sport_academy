# Generated by Django 4.2 on 2024-05-16 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tg_service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='password1',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='password2',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='children',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tg_service.parents'),
        ),
    ]