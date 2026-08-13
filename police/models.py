
from django.db import models

class Employee(models.Model):
    RANKS = [
        ("سرباز", "سرباز"), ("درجه‌دار", "درجه‌دار"),
        ("ستوان سوم", "ستوان سوم"), ("ستوان دوم", "ستوان دوم"),
        ("ستوان یکم", "ستوان یکم"), ("سروان", "سروان"),
        ("سرگرد", "سرگرد"), ("سرهنگ دوم", "سرهنگ دوم"),
        ("سرهنگ", "سرهنگ"), ("سرتیپ", "سرتیپ"), ("سردار", "سردار"),
    ]
    STATUS = [
        ("active", "شاغل"), ("leave", "مرخصی"), ("retired", "بازنشسته"),
        ("inactive", "غیرفعال"),
    ]

    first_name = models.CharField("نام", max_length=80)
    last_name = models.CharField("نام خانوادگی", max_length=100)
    personnel_code = models.CharField("کد پرسنلی", max_length=30, unique=True)
    national_code = models.CharField("کد ملی", max_length=10, blank=True)
    age = models.PositiveSmallIntegerField("سن")
    service_years = models.PositiveSmallIntegerField("مقدار خدمت (سال)", default=0)
    service_months = models.PositiveSmallIntegerField("مقدار خدمت (ماه)", default=0)
    rank = models.CharField("مقام / درجه نظامی", max_length=40, choices=RANKS)
    unit = models.CharField("یگان / واحد", max_length=120, blank=True)
    position = models.CharField("سمت", max_length=120, blank=True)
    phone = models.CharField("شماره تماس", max_length=20, blank=True)
    status = models.CharField("وضعیت", max_length=20, choices=STATUS, default="active")
    notes = models.TextField("توضیحات", blank=True)
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)
    updated_at = models.DateTimeField("آخرین ویرایش", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "کارمند"
        verbose_name_plural = "کارکنان"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.personnel_code}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def total_service_months(self):
        return self.service_years * 12 + self.service_months


class ServiceRecord(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name="service_records", verbose_name="کارمند"
    )
    title = models.CharField("عنوان سابقه", max_length=150)
    from_date = models.DateField("از تاریخ")
    to_date = models.DateField("تا تاریخ", null=True, blank=True)
    description = models.TextField("شرح", blank=True)

    class Meta:
        ordering = ["-from_date"]
        verbose_name = "سابقه خدمت"
        verbose_name_plural = "سوابق خدمت"

    def __str__(self):
        return f"{self.employee.full_name} - {self.title}"
