
from django.contrib import admin
from .models import Employee, ServiceRecord

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("personnel_code", "first_name", "last_name", "age", "service_years",
                    "service_months", "rank", "status", "unit")
    search_fields = ("first_name", "last_name", "personnel_code", "national_code", "unit")
    list_filter = ("rank", "status", "unit")

@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ("employee", "title", "from_date", "to_date")
    search_fields = ("employee__first_name", "employee__last_name", "employee__personnel_code", "title")
    list_filter = ("from_date",)
