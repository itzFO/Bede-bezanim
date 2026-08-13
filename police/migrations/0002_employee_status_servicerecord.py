
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("police", "0001_initial")]
    operations = [
        migrations.AddField(
            model_name="employee",
            name="status",
            field=models.CharField(
                choices=[
                    ("active","شاغل"),("leave","مرخصی"),
                    ("retired","بازنشسته"),("inactive","غیرفعال")
                ],
                default="active", max_length=20, verbose_name="وضعیت"
            ),
        ),
        migrations.CreateModel(
            name="ServiceRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150, verbose_name="عنوان سابقه")),
                ("from_date", models.DateField(verbose_name="از تاریخ")),
                ("to_date", models.DateField(blank=True, null=True, verbose_name="تا تاریخ")),
                ("description", models.TextField(blank=True, verbose_name="شرح")),
                ("employee", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="service_records",
                    to="police.employee",
                    verbose_name="کارمند"
                )),
            ],
            options={
                "verbose_name": "سابقه خدمت",
                "verbose_name_plural": "سوابق خدمت",
                "ordering": ["-from_date"],
            },
        ),
    ]
