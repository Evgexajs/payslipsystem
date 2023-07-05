from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculate.as_view(), name='calculate'),
    path('generate-pdf/', views.generate_pdf, name='generate-pdf'),
    path('generate-ndfl/', views.generate_ndfl, name='generate-ndfl'),

    # path('departments/', views.departments, name='departments'),
    # path('positions/', views.positions, name='positions'),
    # path('employees/', views.employees, name='employees'),
    # path('salary-types/', views.salary_types, name='salary_types'),
    # path('taxes/', views.taxes, name='taxes'),
    # path('tax-payments/', views.tax_payments, name='tax_payments'),
    # path('employee-list/', views.employee_list, name='employee_list'),
    # path('employee-detail/<int:pk>/', views.employee_detail, name='employee_detail'),

    # path('generate-pdf/', views.generate_pdf, name='generate-pdf'),
    # path('ndfl-report/<int:pk>/', views.ndfl_report, name='ndfl-report'),
    # path('tax-reports/', views.tax_reports, name='tax_reports'),
]
