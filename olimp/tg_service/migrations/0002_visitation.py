# Generated by Django 4.2 on 2024-05-24 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tg_service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time_of_arrival', models.TimeField()),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitations', to='tg_service.subscription')),
            ],
            options={
                'db_table': 'visitation',
            },
        ),
    ]