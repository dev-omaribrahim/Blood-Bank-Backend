# Generated by Django 3.2 on 2022-06-20 15:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_serial_number', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='سيريال الفاتورة')),
                ('patient_name', models.CharField(max_length=255, null=True, verbose_name='اسم المريض')),
                ('patient_gender', models.CharField(choices=[('male', 'ذكر'), ('female', 'انثى')], max_length=20, null=True, verbose_name='الجنس')),
                ('patient_age', models.DateField(null=True, verbose_name='تاريخ الميلاد')),
                ('patient_blood_type', models.CharField(choices=[('a_positive', 'A+'), ('a_minus', 'A-'), ('b_positive', 'B+'), ('b_minus', 'B-'), ('o_positive', 'O+'), ('o_minus', 'O-'), ('ab_positive', 'AB+'), ('ab_minus', 'AB-'), ('a_group', 'A'), ('b_group', 'B'), ('o_group', 'O'), ('ab_group', 'AB')], max_length=255, null=True, verbose_name='فصيلة الدم')),
                ('hospital_name', models.CharField(max_length=255, null=True, verbose_name='اسم المستشفى')),
                ('patient_national_id', models.CharField(max_length=255, null=True, verbose_name='الرقم القومى / رقم الباسبور')),
                ('item_quantity', models.PositiveIntegerField(default=1, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='عدد الوحدات')),
                ('total_price', models.DecimalField(blank=True, decimal_places=3, max_digits=7, null=True, verbose_name='سعر الفاتورة')),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='تاريخ الفاتورة')),
            ],
            options={
                'verbose_name': 'الفاتورة',
                'verbose_name_plural': 'الفواتير',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Prices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_type', models.CharField(choices=[('full_blood', 'كيس دم كامل'), ('rbcs', 'RPCs'), ('plasma', 'بلازما'), ('blood_platelets', 'صفائح دموية'), ('cryo', 'cryo')], max_length=100, null=True, verbose_name='نوع الوحدة')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='سعر الوحدة')),
            ],
            options={
                'verbose_name': 'سعر الوحدة',
                'verbose_name_plural': 'اسعار الوحدات',
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_name', models.CharField(max_length=255, verbose_name='اسم المستشفى')),
                ('hospital_phone', models.CharField(max_length=255, null=True, verbose_name='رقم المستشفى')),
                ('hospital_address', models.CharField(max_length=255, null=True, verbose_name='عنوان المستشفى')),
                ('hospital_general_serial_number', models.CharField(max_length=255, verbose_name='سيريال نمبر المستشفى')),
                ('receipt_number', models.PositiveIntegerField(blank=True, null=True, unique=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='رقم الايصال')),
                ('receipt_date', models.DateField(auto_now_add=True, verbose_name='تاريخ الايصال')),
                ('items_quantity', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='عدد الوحدات')),
            ],
            options={
                'verbose_name': 'وصل الشراء',
                'verbose_name_plural': 'وصولات الشراء',
            },
        ),
    ]