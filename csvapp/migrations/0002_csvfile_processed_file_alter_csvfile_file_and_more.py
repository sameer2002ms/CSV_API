# Generated by Django 4.2.6 on 2024-09-19 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csvapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='csvfile',
            name='processed_file',
            field=models.FileField(blank=True, null=True, upload_to='csvs/processed/'),
        ),
        migrations.AlterField(
            model_name='csvfile',
            name='file',
            field=models.FileField(upload_to='csvs/'),
        ),
        migrations.CreateModel(
            name='CSVOperationTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=255)),
                ('operation', models.CharField(max_length=50)),
                ('status', models.CharField(default='PENDING', max_length=20)),
                ('result_file', models.FileField(blank=True, null=True, upload_to='csvs/results/')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csvapp.csvfile')),
            ],
        ),
    ]
