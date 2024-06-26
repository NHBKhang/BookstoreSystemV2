# Generated by Django 5.0.3 on 2024-03-27 15:49

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_book_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book_inventories',
            options={'verbose_name': 'books belong to inventories', 'verbose_name_plural': 'books belong to inventories'},
        ),
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(related_name='books', to='core.author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(related_name='books', to='core.category'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dd0qzygo7/image/upload/v1711539545/gyaplslq1shp2exulcia.png', max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
