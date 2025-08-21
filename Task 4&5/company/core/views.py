from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import F
from .models import Department, Employee, LeaveApplication
from .serializers import DepartmentSerializer, EmployeeSerializer, LeaveApplicationSerializer


# 1. Create Department
@api_view(['POST'])
def create_department(request):
    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. Create Employee
@api_view(['POST'])
def create_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 3. Set Base Salary
@api_view(['POST'])
def set_base_salary(request, emp_id):
    try:
        emp = Employee.objects.get(id=emp_id)
        emp.baseSalary = request.data.get("baseSalary")
        emp.save()
        return Response({"message": "Base salary updated", "baseSalary": emp.baseSalary})
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)


# 4. Update Leave Count
@api_view(['PUT'])
def update_leave(request, emp_id):
    try:
        leave_obj, created = LeaveApplication.objects.get_or_create(
            employee_id=emp_id,
            month=request.data.get("month"),
            year=request.data.get("year"),
            defaults={'leaves': request.data.get("leaves", 0)}
        )
        if not created:
            leave_obj.leaves = F('leaves') + request.data.get("leaves", 0)
            leave_obj.save()
        return Response({"message": "Leave count updated"})
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)


# 5. Calculate Payable Salary
@api_view(['POST'])
def calculate_salary(request, emp_id):
    month = request.data.get("month")
    year = request.data.get("year")

    try:
        emp = Employee.objects.get(id=emp_id)
        leave = LeaveApplication.objects.filter(employee=emp, month=month, year=year).first()
        leave_count = leave.leaves if leave else 0

        payable = emp.baseSalary - (leave_count * (emp.baseSalary // 25))
        return Response({
            "employee": emp.name,
            "baseSalary": emp.baseSalary,
            "leaves": leave_count,
            "payableSalary": payable
        })
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)


# 6. High Earners in Department
@api_view(['GET'])
def high_earners_department(request, dept_id):
    salaries = list(Employee.objects.filter(department_id=dept_id).values_list("baseSalary", flat=True).distinct())
    top_salaries = sorted(salaries, reverse=True)[:3]

    employees = Employee.objects.filter(department_id=dept_id, baseSalary__in=top_salaries)
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)


# 7. High Earners in Specific Month (Payable Salary wise)
@api_view(['GET'])
def high_earners_month(request, month, year, dept_id):
    employees = Employee.objects.filter(department_id=dept_id)
    data = []

    for emp in employees:
        leave = LeaveApplication.objects.filter(employee=emp, month=month, year=year).first()
        leave_count = leave.leaves if leave else 0
        payable = emp.baseSalary - (leave_count * (emp.baseSalary // 25))
        data.append({"employee": emp.name, "payableSalary": payable})

    top_salaries = sorted({d["payableSalary"] for d in data}, reverse=True)[:3]
    result = [d for d in data if d["payableSalary"] in top_salaries]

    return Response(result)

# core/views.py (append)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .mongo import get_collection

@api_view(["GET"])
def chat_history(request, dept_uuid):
    """
    GET /api/department/<uuid:dept_uuid>/chat/history/?limit=50
    Returns last N messages for department group
    """
    limit = int(request.GET.get("limit", 50))
    coll = get_collection()
    cursor = coll.find({"group": str(dept_uuid)}).sort("ts", -1).limit(limit)
    items = list(cursor)
    # Remove Mongo _id for clean output
    for x in items:
        x.pop("_id", None)
    return Response(list(reversed(items)))

# testapp/views.py
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, Django is working!")