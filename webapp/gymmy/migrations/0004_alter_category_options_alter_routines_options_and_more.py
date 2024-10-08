# Generated by Django 5.1 on 2024-09-01 09:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymmy', '0003_category_routines'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='routines',
            options={'verbose_name_plural': 'routines'},
        ),
        migrations.AddField(
            model_name='routines',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favourite_routines', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='routines',
            name='description',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
    ]
