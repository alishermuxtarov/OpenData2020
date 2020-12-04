from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Время обновления')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_regions', to=settings.AUTH_USER_MODEL, verbose_name='Создано пользоветем')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_regions', to=settings.AUTH_USER_MODEL, verbose_name='Обновлено пользоветем')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
                'db_table': 'reference_regions',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Время обновления')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_areas', to=settings.AUTH_USER_MODEL, verbose_name='Создано пользоветем')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='reference.Region', verbose_name='Регион')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_areas', to=settings.AUTH_USER_MODEL, verbose_name='Обновлено пользоветем')),
            ],
            options={
                'verbose_name': 'Город/Район',
                'verbose_name_plural': 'Города/Районы',
                'db_table': 'reference_areas',
                'ordering': ['-id'],
            },
        ),
    ]
