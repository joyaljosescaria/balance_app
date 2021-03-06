# Generated by Django 3.0.7 on 2020-06-08 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amount_debit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit_use', models.CharField(max_length=50)),
                ('debit_amt', models.FloatField()),
                ('debited_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.IntegerField(null=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Service_sites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=50)),
                ('site_address', models.CharField(max_length=50)),
                ('site_desc', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Total',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amt', models.FloatField()),
                ('profit_total', models.FloatField()),
                ('loss_total', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=50)),
                ('service_charge', models.FloatField()),
                ('profit', models.FloatField()),
                ('isPaid', models.BooleanField()),
                ('paid_amt', models.FloatField()),
                ('service_date', models.DateField(auto_now=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calcbook.Customers')),
            ],
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance_amt', models.FloatField()),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calcbook.Services')),
            ],
        ),
    ]
