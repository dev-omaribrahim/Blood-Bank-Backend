# Generated by Django 3.2 on 2022-06-20 15:49

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("money_manage_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseDonation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "donation_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("inside_donation", "تبرع داخلى"),
                            ("outside_donation", "تبرع خارجى"),
                            ("replace_donation", "تبرع إستبدال"),
                        ],
                        max_length=255,
                        null=True,
                        verbose_name="نوع التبرع",
                    ),
                ),
                (
                    "unit_type",
                    models.CharField(
                        choices=[
                            ("full_blood", "كيس دم كامل"),
                            ("rbcs", "RPCs"),
                            ("plasma", "بلازما"),
                            ("blood_platelets", "صفائح دموية"),
                            ("cryo", "cryo"),
                        ],
                        max_length=255,
                        verbose_name="نوع الوحدة",
                    ),
                ),
                (
                    "blood_type",
                    models.CharField(
                        choices=[
                            ("a_positive", "A+"),
                            ("a_minus", "A-"),
                            ("b_positive", "B+"),
                            ("b_minus", "B-"),
                            ("o_positive", "O+"),
                            ("o_minus", "O-"),
                            ("ab_positive", "AB+"),
                            ("ab_minus", "AB-"),
                            ("a_group", "A"),
                            ("b_group", "B"),
                            ("o_group", "O"),
                            ("ab_group", "AB"),
                        ],
                        max_length=255,
                        verbose_name="فصيلة الدم",
                    ),
                ),
                (
                    "unit_quantity",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="عدد الوحدات",
                    ),
                ),
                (
                    "unit_serial_number",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="سيريال الوحدة",
                    ),
                ),
                (
                    "pipe_serial_number",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="سيريال الخرطوم",
                    ),
                ),
                (
                    "donation_create_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="تاريخ التبرع"
                    ),
                ),
                (
                    "donation_create_date_on_system",
                    models.DateField(
                        auto_now_add=True,
                        null=True,
                        verbose_name="تاريخ ادخال التبرع على السيستم",
                    ),
                ),
                (
                    "donation_expiration_scope",
                    models.PositiveIntegerField(
                        choices=[
                            (35, "35 يوم"),
                            (42, "42 يوم"),
                            (180, "180 يوم"),
                            (365, "365 يوم"),
                            (5, "5 ايام"),
                        ],
                        null=True,
                        verbose_name="مدة صلاحية الوحدة",
                    ),
                ),
                (
                    "donation_expire_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="تاريخ انتهاء الصلاحية"
                    ),
                ),
                (
                    "analyse_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("pending", "pending"),
                            ("free", "free"),
                            ("damaged", "damaged"),
                        ],
                        max_length=255,
                        null=True,
                        verbose_name="نتيجة تحليل الوحدة",
                    ),
                ),
                (
                    "unit_notes",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("place_holder1", "place holder 1"),
                            ("place_holder2", "place holder 2"),
                        ],
                        max_length=255,
                        null=True,
                        verbose_name="ملاحظات عن الوحدة",
                    ),
                ),
                (
                    "unit_exchange_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("available_for_exchange", "قابل للصرف"),
                            ("not_available_for_exchange", "غير قابل للصرف"),
                            ("executed", "معدم"),
                        ],
                        max_length=255,
                        null=True,
                        verbose_name="حالة الصرف",
                    ),
                ),
                (
                    "is_sold",
                    models.BooleanField(
                        blank=True,
                        default=False,
                        null=True,
                        verbose_name="هل تم بيعه ؟",
                    ),
                ),
                (
                    "is_separable",
                    models.BooleanField(
                        blank=True,
                        default=False,
                        null=True,
                        verbose_name="هل قابلة للفصل ؟",
                    ),
                ),
                (
                    "unit_bill",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="basedonation_related",
                        to="money_manage_app.bill",
                        verbose_name="الفاتورة",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Derivation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DonationExpirationScope",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "scope_label",
                    models.CharField(
                        max_length=100,
                        null=True,
                        unique=True,
                        verbose_name="تعريف المدة",
                    ),
                ),
                (
                    "scope_days",
                    models.PositiveIntegerField(
                        default=1,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="عدد ايام الصلاحية",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DonorProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "full_name",
                    models.CharField(max_length=255, verbose_name="الاسم بالكامل"),
                ),
                ("age", models.DateField(verbose_name="السن")),
                (
                    "phone_number",
                    models.CharField(max_length=11, verbose_name="رقم الموبايل"),
                ),
                ("address", models.CharField(max_length=255, verbose_name="العنوان")),
                (
                    "national_id",
                    models.PositiveIntegerField(
                        unique=True, verbose_name="رقم البطاقة او الباسبور"
                    ),
                ),
                (
                    "blood_type",
                    models.CharField(
                        choices=[
                            ("a_positive", "A+"),
                            ("a_minus", "A-"),
                            ("b_positive", "B+"),
                            ("b_minus", "B-"),
                            ("o_positive", "O+"),
                            ("o_minus", "O-"),
                            ("ab_positive", "AB+"),
                            ("ab_minus", "AB-"),
                        ],
                        default="a_positive",
                        max_length=50,
                        verbose_name="فصيلة الدم",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "ذكر"), ("female", "انثى")],
                        default="male",
                        max_length=20,
                        verbose_name="الجنس",
                    ),
                ),
                (
                    "created_at",
                    models.DateField(
                        auto_now_add=True, null=True, verbose_name="وقت انشاء الملف"
                    ),
                ),
            ],
            options={
                "verbose_name": "ملف الشخصي للمتبرع",
                "verbose_name_plural": "الملفات الشخصية للمتبرعين",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="InstituteProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "full_name",
                    models.CharField(max_length=255, verbose_name="اسم المنشأة"),
                ),
                (
                    "phone_number",
                    models.CharField(max_length=11, verbose_name="رقم الهاتف"),
                ),
                ("address", models.CharField(max_length=255, verbose_name="العنوان")),
                (
                    "created_at",
                    models.DateField(
                        auto_now_add=True, null=True, verbose_name="وقت انشاء الجهة"
                    ),
                ),
            ],
            options={
                "verbose_name": "ملف الجهة المتبرعة",
                "verbose_name_plural": "ملفات الجهات المتبرعة",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="ReplaceDonation",
            fields=[
                (
                    "basedonation_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="donation_app.basedonation",
                    ),
                ),
                (
                    "operation_type",
                    models.CharField(
                        choices=[("import", "استيراد"), ("export", "تصدير")],
                        max_length=255,
                        null=True,
                        verbose_name="نوع الاستبدال",
                    ),
                ),
                (
                    "external_serial_number",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="السيريال نمبر الخارجى للتبرع",
                    ),
                ),
                (
                    "institute_profile",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="replace_institute_donation",
                        to="donation_app.instituteprofile",
                    ),
                ),
            ],
            options={
                "verbose_name": "تبرع الإستبدال",
                "verbose_name_plural": "تبرعات الإستبدال",
            },
            bases=("donation_app.basedonation",),
        ),
        migrations.CreateModel(
            name="OutsideDonation",
            fields=[
                (
                    "basedonation_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="donation_app.basedonation",
                    ),
                ),
                (
                    "general_serial_number",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="السيريال نمبر الخاص بالمنشأة",
                    ),
                ),
                (
                    "receipt",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="donated_units",
                        to="money_manage_app.receipt",
                        verbose_name="إيصال الشراء",
                    ),
                ),
            ],
            options={
                "verbose_name": "التبرع الخارجى",
                "verbose_name_plural": "التبرعات الخارجية",
            },
            bases=("donation_app.basedonation",),
        ),
        migrations.CreateModel(
            name="InsideDonation",
            fields=[
                (
                    "basedonation_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="donation_app.basedonation",
                    ),
                ),
                (
                    "used_for_deriving",
                    models.BooleanField(
                        default=False, verbose_name="هل تم الاشتقاق منها من قبل ؟"
                    ),
                ),
                (
                    "is_derivative",
                    models.BooleanField(default=False, verbose_name="هل هى مشتقة ؟"),
                ),
                (
                    "donor_profile",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="personal_donation",
                        to="donation_app.donorprofile",
                        verbose_name="ملف المتبرع",
                    ),
                ),
                (
                    "parents",
                    models.ManyToManyField(
                        blank=True,
                        related_name="derivatives",
                        through="donation_app.Derivation",
                        to="donation_app.InsideDonation",
                        verbose_name="الوحدة المشتقة منها",
                    ),
                ),
            ],
            options={
                "verbose_name": "التبرع الداخلى",
                "verbose_name_plural": "التبرعات الداخلية",
            },
            bases=("donation_app.basedonation",),
        ),
        migrations.AddField(
            model_name="derivation",
            name="child",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="parent_derivation",
                to="donation_app.insidedonation",
                verbose_name="المشتق",
            ),
        ),
        migrations.AddField(
            model_name="derivation",
            name="parent",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="child_derivation",
                to="donation_app.insidedonation",
                verbose_name="تم الاشتقاق من",
            ),
        ),
    ]
