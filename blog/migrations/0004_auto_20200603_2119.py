# Generated by Django 3.0.6 on 2020-06-03 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.ImageStorage'),
        ),
    ]
