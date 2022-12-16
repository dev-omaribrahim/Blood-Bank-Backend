from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from money_manage_app.models import Bill, Receipt
from datetime import timedelta, datetime
import random
from .utils import blood_convert_dict, generate_serial_number
from . import choices


class BaseDonation(models.Model):
    """
    Base class for all donation types: it holds all general
    and shared fields among the three types
    """
    donation_type = models.CharField(
        max_length=255, choices=choices.DONATION_TYPE_CHOICES,
        null=True, blank=True, verbose_name="نوع التبرع"
    )
    unit_type = models.CharField(
        max_length=255, choices=choices.UNIT_TYPE_CHOICES,
        null=False, blank=False, verbose_name="نوع الوحدة"
    )
    blood_type = models.CharField(
        max_length=255, choices=choices.BLOOD_TYPE_CHOICES,
        null=False, blank=False, verbose_name="فصيلة الدم"
    )
    unit_quantity = models.PositiveIntegerField(
        null=False, blank=False, default=1,
        validators=[MinValueValidator(1)], verbose_name="عدد الوحدات"
    )
    unit_serial_number = models.CharField(
        max_length=255, unique=True,
        null=True, blank=True, verbose_name="سيريال الوحدة"
    )
    pipe_serial_number = models.CharField(
        max_length=255, unique=True,
        null=True, blank=True, verbose_name="سيريال الخرطوم"
    )
    donation_create_date = models.DateField(
        null=True, blank=True, verbose_name="تاريخ التبرع"
    )
    donation_create_date_on_system = models.DateField(
        auto_now_add=True, verbose_name="تاريخ ادخال التبرع على السيستم",
        null=True, blank=True
    )
    donation_expiration_scope = models.PositiveIntegerField(
        choices=choices.DONATION_EXPIRATION_SCOPE_CHOICES,
        null=True, blank=False, verbose_name="مدة صلاحية الوحدة"
    )
    donation_expire_date = models.DateField(
        null=True, blank=True, verbose_name="تاريخ انتهاء الصلاحية"
    )
    analyse_status = models.CharField(
        max_length=255, null=True, blank=True,
        choices=choices.ANALYSE_STATUS, verbose_name="نتيجة تحليل الوحدة"
    )
    unit_notes = models.CharField(
        max_length=255, choices=choices.UNITE_NOTES_CHOICES,
        null=True, blank=True, verbose_name="ملاحظات عن الوحدة"
    )
    unit_exchange_status = models.CharField(
        max_length=255, choices=choices.EXCHANGE_STATUS_CHOICES,
        null=True, blank=True, verbose_name="حالة الصرف"
    )
    unit_bill = models.ForeignKey(
        Bill, related_name="%(class)s_related",
        on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الفاتورة"
    )
    is_sold = models.BooleanField(
        null=True, blank=True, default=False,
        verbose_name="هل تم بيعه ؟"
    )
    is_separable = models.BooleanField(
        null=True, blank=True, default=False,
        verbose_name="هل قابلة للفصل ؟"
    )

    def blood_mapper(self):
        self.blood_type = blood_convert_dict[self.blood_type]
        return self.blood_type

    def save(self, *args, **kwargs):
        self.donation_expire_date = self.donation_create_date + timedelta(days=self.donation_expiration_scope)

        if self.unit_type == choices.PLASMA or self.unit_type == choices.BLOOD_PLATELETS or self.unit_type == choices.CRYO:
            self.blood_mapper()

        if not self.unit_serial_number:
            random_num = random.randint(234567, 789000)
            exists_objs = BaseDonation.objects.filter(unit_serial_number=random_num)

            while exists_objs:
                random_num = random.randint(234567, 789000)
            else:
                self.unit_serial_number = "{}-{}".format(self.donation_type, random_num)
            # self.unit_serial_number = generate_serial_number(self)

        if self.analyse_status == choices.FREE:
            self.unit_exchange_status = choices.AVAILABLE_FOR_EXCHANGE
        else:
            self.unit_exchange_status = choices.NOT_AVAILABLE_FOR_EXCHANGE

        super().save(*args, **kwargs)


class InsideDonation(BaseDonation):
    donor_profile = models.ForeignKey(
        "DonorProfile", related_name="personal_donation",
        on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="ملف المتبرع"
    )
    used_for_deriving = models.BooleanField(
        default=False, null=False, blank=False,
        verbose_name="هل تم الاشتقاق منها من قبل ؟"
    )
    is_derivative = models.BooleanField(
        default=False, null=False, blank=False,
        verbose_name="هل هى مشتقة ؟"
    )
    parents = models.ManyToManyField(
        "self", symmetrical=False, related_name="derivatives",
        through="Derivation", blank=True,
        verbose_name="الوحدة المشتقة منها"
    )

    class Meta:
        verbose_name = "التبرع الداخلى"
        verbose_name_plural = "التبرعات الداخلية"

    def save(self, *args, **kwargs):
        if (self.unit_type == choices.FULL_BLOOD or self.unit_type == choices.PLASMA) and \
                not self.used_for_deriving and self.analyse_status == choices.FREE:
            self.is_separable = True
        else:
            self.is_separable = False

        if not self.analyse_status:
            self.analyse_status = choices.PENDING
        self.donation_type = choices.INSIDE_DONATION
        return super().save(*args, **kwargs)

    def __str__(self):
        return "{} / {}".format(
            # InsideDonation._meta.get_field("donation_type").verbose_name,
            self.get_unit_type_display(),
            self.get_donation_type_display()
        )


class Derivation(models.Model):
    """
    hold the info for derivation process,
    you can add more info if needed later
    """
    parent = models.ForeignKey(
        InsideDonation, related_name="child_derivation",
        on_delete=models.SET_NULL, null=True,
        verbose_name="تم الاشتقاق من"
    )
    child = models.ForeignKey(
        InsideDonation, related_name="parent_derivation",
        on_delete=models.SET_NULL, null=True,
        verbose_name="المشتق"
    )


class OutsideDonation(BaseDonation):
    receipt = models.ForeignKey(
        Receipt, related_name="donated_units",
        on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name="إيصال الشراء"
    )
    general_serial_number = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name="السيريال نمبر الخاص بالمنشأة"
    )

    class Meta:
        verbose_name = "التبرع الخارجى"
        verbose_name_plural = "التبرعات الخارجية"

    def save(self, *args, **kwargs):
        self.donation_type = choices.OUTSIDE_DONATION

        if not self.analyse_status:
            self.analyse_status = choices.FREE

        self.is_separable = False
        return super().save(*args, **kwargs)

    def __str__(self):
        return "{} / {}".format(
            self.get_unit_type_display(),
            self.get_donation_type_display()
        )


class ReplaceDonation(BaseDonation):
    operation_type = models.CharField(
        max_length=255, choices=choices.OPERATION_TYPE,
        null=True, blank=False, verbose_name="نوع الاستبدال"
    )
    institute_profile = models.ForeignKey(
        "InstituteProfile", related_name="replace_institute_donation",
        on_delete=models.SET_NULL, null=True, blank=False
    )
    external_serial_number = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name="السيريال نمبر الخارجى للتبرع"
    )

    class Meta:
        verbose_name = "تبرع الإستبدال"
        verbose_name_plural = "تبرعات الإستبدال"

    def save(self, *args, **kwargs):
        self.donation_type = choices.REPLACE_DONATION

        if not self.analyse_status:
            self.analyse_status = choices.FREE

        self.is_separable = False
        return super().save(*args, **kwargs)

    def __str__(self):
        return "{} / {}".format(
            self.get_unit_type_display(),
            self.get_donation_type_display()
        )


class DonorProfile(models.Model):
    full_name = models.CharField(
        max_length=255, null=False, blank=False,
        verbose_name="الاسم بالكامل"
    )
    age = models.DateField(
        null=False, blank=False, verbose_name="السن"
    )
    phone_number = models.CharField(
        max_length=11, null=False, blank=False,
        verbose_name="رقم الموبايل"
    )
    address = models.CharField(
        max_length=255, null=False, blank=False,
        verbose_name="العنوان"
    )
    national_id = models.PositiveIntegerField(
        unique=True, null=False, blank=False,
        verbose_name="رقم البطاقة او الباسبور"
    )

    blood_type = models.CharField(
        max_length=50, null=False, blank=False,
        choices=choices.DONOR_BLOOD_TYPE_CHOICES, default=choices.A_POSITIVE,
        verbose_name="فصيلة الدم"
    )
    gender = models.CharField(
        max_length=20, null=False, blank=False,
        choices=choices.GENDER_CHOICES, default=choices.MALE,
        verbose_name="الجنس"
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name="وقت انشاء الملف",
        null=True, blank=False
    )

    class Meta:
        verbose_name = "ملف الشخصي للمتبرع"
        verbose_name_plural = "الملفات الشخصية للمتبرعين"
        ordering = ("-created_at",)

    def __str__(self):
        return "{} / {}".format(
            self.full_name,
            self.national_id
        )


class InstituteProfile(models.Model):
    full_name = models.CharField(
        max_length=255, null=False, blank=False,
        verbose_name="اسم المنشأة"
    )
    phone_number = models.CharField(
        max_length=11, null=False, blank=False,
        verbose_name="رقم الهاتف"
    )
    address = models.CharField(
        max_length=255, null=False, blank=False,
        verbose_name="العنوان"
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name="وقت انشاء الجهة",
        null=True, blank=False
    )

    class Meta:
        verbose_name = "ملف الجهة المتبرعة"
        verbose_name_plural = "ملفات الجهات المتبرعة"
        ordering = ("-created_at",)

    def __str__(self):
        return "{}".format(
            self.full_name,
        )


class DonationExpirationScope(models.Model):
    scope_label = models.CharField(
        max_length=100, null=True, blank=False,
        unique=True, verbose_name="تعريف المدة"
    )

    scope_days = models.PositiveIntegerField(
        null=True, blank=False, default=1,
        validators=[MinValueValidator(1)],
        verbose_name="عدد ايام الصلاحية"
    )
