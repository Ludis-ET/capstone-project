# Generated by Django 5.0.3 on 2024-03-16 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_cover_page_book_coverpage'),
        ('user', '0011_alter_customuser_is_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelf',
            name='books',
            field=models.ManyToManyField(blank=True, related_name='shelves', to='core.book'),
        ),
    ]
