# from django import forms
# from .models import SalaryPayment, Department, Position, Employee, SalaryType, Tax, TaxPayment


# class SalaryPaymentForm(forms.ModelForm):
#     class Meta:
#         model = SalaryPayment
#         fields = ['employee', 'salary_type', 'year', 'month', 'amount']
#         labels = {
#             'employee': 'Сотрудник',
#             'salary_type': 'Тип заработной платы',
#             'year': 'Год',
#             'month': 'Месяц',
#             'amount': 'Сумма',
#         }
#         widgets = {
#             'employee': forms.Select(attrs={'class': 'form-control', 'style': 'display: block'}),
#             'salary_type': forms.Select(attrs={'class': 'form-control', 'style': 'display: block'}),
#             'year': forms.NumberInput(attrs={'class': 'form-control', 'style': 'display: block'}),
#             'month': forms.NumberInput(attrs={'class': 'form-control', 'style': 'display: block'}),
#             'amount': forms.NumberInput(attrs={'class': 'form-control', 'style': 'display: block'}),
#         }

# class DepartmentForm(forms.ModelForm):
#     class Meta:
#         model = Department
#         fields = ['name']
#         labels = {
#             'name': 'Название'
#         }
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'display: block'}),
#         }

# class PositionForm(forms.ModelForm):
#     class Meta:
#         model = Position
#         fields = ['name']
#         labels = {
#             'name': 'Название'
#         }
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'display: block'}),
#         }

# class EmployeeForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#         fields = ['full_name', 'department', 'position']
#         labels = {
#             'full_name': 'ФИО',
#             'department': 'Департамент',
#             'position': 'Должность'
#         }
#         widgets = {
#             'full_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'display: block'}),
#             'department': forms.Select(attrs={'class': 'form-control', 'style': 'display: block'}),
#             'position': forms.Select(attrs={'class': 'form-control', 'style': 'display: block'}),
#         }
        
# class SalaryTypeForm(forms.ModelForm):
#     class Meta:
#         model = SalaryType
#         fields = ['name', 'description']
#         labels = {
#             'name': 'Название',
#             'description': 'Описание',
#         }
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'display: block'}),
#             'description': forms.TextInput(attrs={'class': 'form-control', 'style': 'display: block'}),
#         }
        
# class TaxForm(forms.ModelForm):
#     class Meta:
#         model = Tax
#         fields = ['name', 'rate', 'description']
#         labels = {
#             'name': 'Название',
#             'rate': 'Доля',
#             'description': 'Описание',
#         }
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'display: block'}),
#             'rate': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'style': 'display: block'}),
#             'description': forms.TextInput(attrs={'class': 'form-control', 'style': 'display: block'}),
#         }
                
# class TaxPaymentForm(forms.ModelForm):
#     class Meta:
#         model = TaxPayment
#         fields = ['employee', 'tax', 'year', 'month', 'amount']
#         labels = {
#             'employee': 'Сотрудник',
#             'tax': 'Налог',
#             'year': 'Год',
#             'month': 'Месяц',
#             'amount': 'Сумма',
#         }
#         widgets = {
#             'employee': forms.Select(attrs={'class': 'form-control', 'style': 'display: block'}),
#             'tax': forms.Select(attrs={'class': 'form-control', 'style': 'display: block'}),
#             'year': forms.NumberInput(attrs={'class': 'form-control', 'style': 'display: block'}),
#             'month': forms.NumberInput(attrs={'class': 'form-control', 'style': 'display: block'}),
#             'amount': forms.NumberInput(attrs={'class': 'form-control', 'style': 'display: block'}),
#         }