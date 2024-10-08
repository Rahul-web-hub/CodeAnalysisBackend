# Generated by Django 5.0.7 on 2024-07-19 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeetcodeProblem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_id', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=255)),
                ('acceptance', models.CharField(max_length=10)),
                ('difficulty', models.CharField(max_length=10)),
                ('frequency', models.FloatField()),
                ('leetcode_link', models.URLField()),
                ('company', models.CharField(max_length=100)),
            ],
        ),
    ]
