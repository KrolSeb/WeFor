from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteCity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country_code', models.CharField(max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Favourite cities',
            },
        ),
        migrations.CreateModel(
            name='PolishCity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('country_code', models.CharField(max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Polish cities',
            },
        ),
        migrations.CreateModel(
            name='WorldwideCity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('country_code', models.CharField(max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Worldwide cities',
            },
        ),
    ]
