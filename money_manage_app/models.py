import random

from django.core.validators import MinValueValidator
from django.db import models

from donation_app import choices


class Bill(models.Model):
    bill_serial_number = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name="سيريال الفاتورة",
    )
    patient_name = models.CharField(
        max_length=255, verbose_name="اسم المريض", null=True, blank=False
    )
    patient_gender = models.CharField(
        choices=choices.GENDER_CHOICES,
        max_length=20,
        null=True,
        blank=False,
        verbose_name="الجنس",
    )
    patient_age = models.DateField(null=True, blank=False, verbose_name="تاريخ الميلاد")
    patient_blood_type = models.CharField(
        max_length=255,
        choices=choices.BLOOD_TYPE_CHOICES,
        null=True,
        blank=False,
        verbose_name="فصيلة الدم",
    )
    hospital_name = models.CharField(
        max_length=255, verbose_name="اسم المستشفى", null=True, blank=False
    )
    patient_national_id = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        verbose_name="الرقم القومى / رقم الباسبور",
    )
    item_quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        null=True,
        blank=False,
        verbose_name="عدد الوحدات",
    )
    total_price = models.DecimalField(
        max_digits=7,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="سعر الفاتورة",
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name="تاريخ الفاتورة", null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.bill_serial_number:
            random_num = random.randint(234567, 789000)
            exists_objs = Bill.objects.filter(bill_serial_number=random_num)

            while exists_objs:
                random_num = random.randint(234567, 789000)
            else:
                self.bill_serial_number = random_num
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "الفاتورة"
        verbose_name_plural = "الفواتير"
        ordering = ("-created_at",)


class Receipt(models.Model):
    hospital_name = models.CharField(
        max_length=255, null=False, blank=False, verbose_name="اسم المستشفى"
    )
    hospital_phone = models.CharField(
        max_length=255, null=True, blank=False, verbose_name="رقم المستشفى"
    )
    hospital_address = models.CharField(
        max_length=255, null=True, blank=False, verbose_name="عنوان المستشفى"
    )
    hospital_general_serial_number = models.CharField(
        max_length=255, null=False, blank=False, verbose_name="سيريال نمبر المستشفى"
    )
    receipt_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        unique=True,
        null=True,
        blank=True,
        verbose_name="رقم الايصال",
    )
    receipt_date = models.DateField(auto_now_add=True, verbose_name="تاريخ الايصال")
    items_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
        verbose_name="عدد الوحدات",
    )

    class Meta:
        verbose_name = "وصل الشراء"
        verbose_name_plural = "وصولات الشراء"

    def save(self, *args, **kwargs):

        if not self.receipt_number:
            random_num = random.randint(234567, 789000)
            exists_objs = Receipt.objects.filter(receipt_number=random_num)
            while exists_objs:
                random_num = random.randint(234567, 789000)
            else:
                self.receipt_number = random_num

            qs = self.donated_units.all()

            if qs.exists():
                self.items_quantity = qs.count()

        return super().save(*args, **kwargs)

    def __str__(self):
        return " رقم الايصال: {}".format(
            self.receipt_number,
        )


class Prices(models.Model):
    unit_type = models.CharField(
        max_length=100,
        choices=choices.UNIT_TYPE_CHOICES,
        verbose_name="نوع الوحدة",
        null=True,
        blank=False,
    )
    unit_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=False,
        verbose_name="سعر الوحدة",
    )

    class Meta:
        verbose_name = "سعر الوحدة"
        verbose_name_plural = "اسعار الوحدات"

    def __str__(self):
        return "{}: {}".format(self.unit_type, self.unit_price)
