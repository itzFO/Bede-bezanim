from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=80, verbose_name="نام")),
                ("last_name", models.CharField(max_length=100, verbose_name="نام خانوادگی")),
                ("personnel_code", models.CharField(max_length=30, unique=True, verbose_name="کد پرسنلی")),
                ("national_code", models.CharField(blank=True, max_length=10, verbose_name="کد ملی")),
                ("age", models.PositiveSmallIntegerField(verbose_name="سن")),
                ("service_years", models.PositiveSmallIntegerField(default=0, verbose_name="مقدار خدمت (سال)")),
                ("service_months", models.PositiveSmallIntegerField(default=0, verbose_name="مقدار خدمت (ماه)")),
                ("rank", models.CharField(choices=[
                    ("سرباز","سرباز"),("درجه‌دار","درجه‌دار"),("ستوان سوم","ستوان سوم"),
                    ("ستوان دوم","ستوان دوم"),("ستوان یکم","ستوان یکم"),("سروان","سروان"),
                    ("سرگرد","سرگرد"),("سرهنگ دوم","سرهنگ دوم"),("سرهنگ","سرهنگ"),
                    ("سرتیپ","سرتیپ"),("سردار","سردار")
                ], max_length=40, verbose_name="مقام / درجه نظامی")),
                ("unit", models.CharField(blank=True, max_length=120, verbose_name="یگان / واحد")),
                ("position", models.CharField(blank=True, max_length=120, verbose_name="سمت")),
                ("phone", models.CharField(blank=True, max_length=20, verbose_name="شماره تماس")),
                ("notes", models.TextField(blank=True, verbose_name="توضیحات")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="آخرین ویرایش")),
            ],
            options={"verbose_name":"کارمند","verbose_name_plural":"کارکنان","ordering":["-created_at"]},
        )
    ]
