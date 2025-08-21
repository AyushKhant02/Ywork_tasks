# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("department/", views.create_department),   # POST: create department
    path("employee/", views.create_employee),       # POST: create employee
    path("employee/<int:emp_id>/salary/", views.set_base_salary),  # POST
    path("employee/<int:emp_id>/leave/", views.update_leave),      # PUT
    path("employee/<int:emp_id>/payable/", views.calculate_salary),# POST
    path("department/<uuid:dept_id>/high-earners/", views.high_earners_department), # GET
    path("department/<uuid:dept_id>/high-earners/<str:month>/<str:year>/", views.high_earners_month), # GET
    path("department/<uuid:dept_uuid>/chat/history/", views.chat_history), # GET chat history
    
]

