
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeForm, RegisterForm, ServiceRecordForm
from .models import Employee, ServiceRecord

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", "")
        )
        if user:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "نام کاربری یا رمز عبور صحیح نیست.")
    return render(request, "registration/login.html")

def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            form.add_error("username", "این نام کاربری قبلاً ثبت شده است.")
        else:
            user = User.objects.create_user(username=username, password=form.cleaned_data["password1"])
            login(request, user)
            return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    qs = Employee.objects.all()
    context = {
        "total": qs.count(),
        "active": qs.filter(status="active").count(),
        "leave": qs.filter(status="leave").count(),
        "retired": qs.filter(status="retired").count(),
        "avg_age": round(sum(e.age for e in qs) / qs.count(), 1) if qs.exists() else 0,
        "total_service": sum(e.total_service_months for e in qs),
        "recent": qs[:6],
    }
    return render(request, "police/dashboard.html", context)

@login_required
def employee_list(request):
    q = request.GET.get("q", "").strip()
    rank = request.GET.get("rank", "").strip()
    status = request.GET.get("status", "").strip()
    employees = Employee.objects.all()
    if q:
        employees = employees.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(personnel_code__icontains=q) | Q(unit__icontains=q)
        )
    if rank:
        employees = employees.filter(rank=rank)
    if status:
        employees = employees.filter(status=status)
    page_obj = Paginator(employees, 12).get_page(request.GET.get("page"))
    return render(request, "police/employee_list.html", {
        "page_obj": page_obj, "q": q, "rank": rank, "status": status,
        "ranks": Employee.RANKS, "statuses": Employee.STATUS,
    })

@login_required
def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        employee = form.save()
        messages.success(request, "اطلاعات کارمند ثبت شد.")
        return redirect("employee_detail", pk=employee.pk)
    return render(request, "police/employee_form.html", {"form": form, "title": "ثبت کارمند جدید"})

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    record_form = ServiceRecordForm()
    return render(request, "police/employee_detail.html", {
        "employee": employee, "record_form": record_form
    })

@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, instance=employee)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "اطلاعات ویرایش شد.")
        return redirect("employee_detail", pk=employee.pk)
    return render(request, "police/employee_form.html", {
        "form": form, "title": "ویرایش اطلاعات کارمند", "employee": employee
    })

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.delete()
        messages.success(request, "رکورد حذف شد.")
        return redirect("employee_list")
    return render(request, "police/employee_confirm_delete.html", {"employee": employee})

@login_required
def service_record_add(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = ServiceRecordForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        record = form.save(commit=False)
        record.employee = employee
        record.save()
        messages.success(request, "سابقه خدمت ثبت شد.")
    return redirect("employee_detail", pk=employee.pk)

@login_required
def service_record_delete(request, pk):
    record = get_object_or_404(ServiceRecord, pk=pk)
    employee_id = record.employee_id
    if request.method == "POST":
        record.delete()
        messages.success(request, "سابقه حذف شد.")
    return redirect("employee_detail", pk=employee_id)

@login_required
def employee_json(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return JsonResponse({
        "id": employee.id,
        "personnel_code": employee.personnel_code,
        "name": employee.full_name,
        "age": employee.age,
        "service_years": employee.service_years,
        "service_months": employee.service_months,
        "rank": employee.rank,
        "status": employee.status,
        "unit": employee.unit,
        "position": employee.position,
    })
