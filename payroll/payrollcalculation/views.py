from django.shortcuts import render, get_object_or_404
from .models import Employee, EmploymentContract, SalaryPayment, Agreement, TimeSheet, Vacation, SickLeave, Violation, Bonus, Company
from django.views import View
from datetime import date
import calendar
import random
from decimal import Decimal

from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
# from reportlab.lib.fonts import addMapping, registerFont, unicodeFonts
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import base64

class calculate(View):
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        months = []
        context = {
            'employees': employees,
            'months': months
        }
        return render(request, 'payroll/calculate.html', context)

    def post(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        months = []
        selected_month = None
        current_month = date.today().month
        current_year = date.today().year

        if request.POST.get('employee') and request.POST.get('month'):
            selected_employee_id = request.POST.get('employee')
            employee = Employee.objects.get(id=selected_employee_id)
            selected_month = request.POST.get('month')
        if request.POST.get('employee'):
            selected_employee_id = request.POST.get('employee')
            employee = Employee.objects.get(id=selected_employee_id)
            contract = EmploymentContract.objects.get(employee=employee)
            start_date = contract.start_date
            start_month = start_date.month
            start_year = start_date.year
            for year in range(start_year, current_year + 1):
                start = start_month if year == start_year else 1
                end = current_month if year == current_year else 12
                for month in range(start, end + 1):
                    months.append(f'{year}-{month}')
        
        context = {
            'employees': employees,
            'selected_employee': employee,
            'selected_month': selected_month,
            'months': months
        }
        return render(request, 'payroll/calculate.html', context)

def generate_pdf(request):
    # получаем данные сотрудника, месяц и год за который нужно произвести расчет
    employee = Employee.objects.get(id=request.GET.get('employee_id'))
    curr_date = request.GET.get('month')
    year = curr_date.split('-')[0]
    month = curr_date.split('-')[1]
    # сформируем дату для корректной работы в виде объекта "дата"
    curr_date = date(int(year), int(month), 1)


    # собираем данные из таблиц БД
    # получаем компанию, она единая но нужна для формирования расчетного листа
    company = Company.objects.get(id=1)

    # получаем договор сотрудника
    contract = EmploymentContract.objects.get(employee=employee)
    # так же под договором могут быть доп соглашения, попытаемся их найти
    # а точне получаем последнее соглашение как действительное
    agreement = None
    agreements = Agreement.objects.filter(contract=contract)
    if agreements:
        agreement = max(agreements, key=lambda x: x.date)
    # действительным контрактом считаем либо последнее соглашение либо первый контракт
    if agreement:
        contract = agreement
    
    # по договору понимаем тип ЗП
    salary_type = contract.salary_type
    # соответственно получаем сколько было выполнено за расчетный период
    time_working = None
    if salary_type == 'fixed' or salary_type == 'hourly':
        time_working = TimeSheet.objects.filter(employee=employee, date=curr_date).first().hours_worked
    else:
        time_working = TimeSheet.objects.filter(employee=employee, date=curr_date).first().piecework_payment

    # дополнительно нужно проверить был ли сотрудник в отпуске за расчетный период
    vacations = Vacation.objects.filter(employee=employee, start_date__year=curr_date.year, start_date__month=curr_date.month)
    # поиск больничных
    sick_leaves = SickLeave.objects.filter(employee=employee, start_date__year=curr_date.year, start_date__month=curr_date.month)
    # поиск нарушений
    violations = Violation.objects.filter(employee=employee, date__year=curr_date.year, date__month=curr_date.month)
    # поиск премий
    bonuses = Bonus.objects.filter(employee=employee, date__year=curr_date.year, date__month=curr_date.month)

    # если оклад фиксированный
    # получаем отдельно ставку на расчет часов которые должны быть отработаны в месяце
    price_for_hour = None
    if salary_type == 'fixed':
        # Получаем количество дней в месяце
        days_in_month = calendar.monthrange(int(year), int(month))[1]
        # Получаем список дней в месяце
        days_list = [date(int(year), int(month), day) for day in range(1, days_in_month+1)]
        # Получаем количество рабочих дней в месяце
        working_days = len([day for day in days_list if day.weekday() < 5])
        price_for_hour = round(contract.salary_rate / working_days / 8, 2)
    else:
        price_for_hour = contract.salary_rate

    # высчитываем сколько заплатить за выполненую работу
    # оба показателя зависят от типа ЗП поэтому если ставка сдельна то расчеты так же будут корректны
    pay_for_working = round(price_for_hour * time_working, 2)
    # доп оплата за отпуск, больничные, премии и вычеты за нарушения
    pay_vacation = 0
    vacation_days = 0
    for vacation in vacations:
        vacation_days += vacation.vacation_days
        pay_vacation += round(contract.salary_rate / Decimal(29.3) * vacation.vacation_days,2)

    pay_sick_leave = 0 # больничный компания платит только за 3 дня и считает по МРОТ
    count_days_sick_leave = 0
    for sick_leave in sick_leaves:
        count_days = sick_leave.days
        if count_days > 3:
            count_days = 3
        count_days_sick_leave += count_days
        pay_sick_leave += round(company.mrot * 24 / 730,2)

    pay_bonus = 0
    for bonus in bonuses:
        pay_bonus += round(bonus.amount,2)
    
    # нарушения, они будут вычитаться
    sum_violation = 0
    for violation in violations:
        sum_violation += round(violation.fine,2)
    # вычеты по законодательству могут происходить только по премии
    pay_bonus = pay_bonus - sum_violation
    if pay_bonus < 0:
        pay_bonus = 0

    # все суммы посчитаны можно вычислить итоговую
    total_pay = round(pay_for_working + pay_vacation + pay_sick_leave + pay_bonus,2)

    # теперь по каждому показателю считаем вычеты - НДФЛ
    pay_for_working_ndfl = 0
    if pay_for_working > 0:
        pay_for_working_ndfl = round(pay_for_working * Decimal(0.13),2)

    pay_vacation_ndfl = 0
    if pay_vacation > 0:
        pay_vacation_ndfl = round(pay_vacation * Decimal(0.13),2)

    pay_sick_leave_ndfl = 0
    if pay_sick_leave > 0:
        pay_sick_leave_ndfl = round(pay_sick_leave * Decimal(0.13),2)

    pay_bonus_ndfl = 0
    if pay_bonus > 0:
        pay_bonus_ndfl = round(pay_bonus * Decimal(0.13),2)

    sum_ndfl = pay_for_working_ndfl + pay_vacation_ndfl + pay_sick_leave_ndfl + pay_bonus_ndfl

    if SalaryPayment.objects.filter(employee=employee, year=year, month=month):
        pass
    else:
        # в результате необходимо создать новый расчетный лист в системе
        SalaryPayment.objects.create(
            employee=employee,
            salary_type=salary_type,
            year=year,
            month=month,
            worked_time=time_working,
            amount=pay_for_working,
            vacation_allowance=pay_vacation,
            sick_leave_allowance=pay_sick_leave,
            bonus=pay_bonus,
            total=total_pay
        )

    # все расчетны произведены, необходимо составить pdf файл
    working_type = ['дни','часы']
    work_days = 0
    if salary_type == 'fixed':
        salary_type = 'Фикс. оклад'
        work_days = round(time_working / 8, 0)
    if salary_type == 'hourly':
        salary_type = 'Почасовая'
        work_days = round(time_working / 8, 0)
    if salary_type == 'piecework':
        working_type = ['','количество']
        salary_type = 'Сдельная'
    # # задаем стиль для таблицы
    styles = getSampleStyleSheet()
    # формируем данные для таблицы
    data = [
        ['Ф.И.О.', employee.full_name, '', '', '', '', '', 'Подразделение', employee.department],
        ['Табельный номер', random.randint(50, 200), '', '', '', '', '',  'Должность', employee.position],
        ['К выплате:', '', '', '', '', '', '',  '', ''],
        ['Вид', salary_type, 'Отработано', '', '', '', 'Сумма (руб)', 'Вид', 'Ставка', 'Сумма (руб)'],
        ['', contract.salary_rate, *working_type, 'дни', 'часы', '', '', ''],
        ['1. Зачислено', '', '', '', '', '', '', '2. Удержано', '', ''],
        ['Оклад по дням', '', work_days, time_working, round(time_working / 8, 0), time_working, pay_for_working,
         'НДФЛ', '0.13', pay_for_working_ndfl],

        ['Премия', '', work_days, time_working, round(time_working / 8, 0), time_working, pay_bonus,
         '', '0.13', pay_bonus_ndfl],

        ['Отпускные', '', vacation_days, round(vacation_days * 8, 0), vacation_days, round(vacation_days * 8, 0), pay_vacation,
         '', '0.13', pay_vacation_ndfl],

        ['Больнычный', '', count_days_sick_leave, round(count_days_sick_leave * 8, 0), count_days_sick_leave, round(count_days_sick_leave * 8, 0), pay_sick_leave,
         '', '0.13', pay_sick_leave_ndfl],

        ['Всего начислено', '', '', '', '', '', total_pay, 'Удержано', '', sum_ndfl],
    ]

    
    # загрузка шрифта
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    # регистрация кириллического шрифта
    pdfmetrics.registerFont(TTFont('Times New Roman Cyr', 'times.ttf'))
    # задаем стиль для таблицы
    style = TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('LINEABOVE', (0,0), (-1,0), 1, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 1, colors.black),
        ('LINEBEFORE', (0,0), (0,-1), 1, colors.black),
        ('LINEAFTER', (-1,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.white),
        ('TEXTCOLOR',(0,0),(-1,0), colors.black),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('FONTNAME', (0,0), (-1,0), 'Times New Roman Cyr'),
        ('FONTSIZE', (0,0), (-1,0), 14),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND',(0,1),(-1,-1),colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman Cyr'),
        ('SPAN', (1, 0), (6, 0)),
        ('SPAN', (8, 0), (9, 0)),
        ('SPAN', (1, 1), (6, 1)),
        ('SPAN', (8, 1), (9, 1)),
        ('SPAN', (0, 2), (6, 2)),
        ('SPAN', (7, 2), (9, 2)),
        ('SPAN', (0, 3), (0, 4)),
        # ('SPAN', (1, 3), (1, 4)),
        ('SPAN', (6, 3), (6, 4)),
        ('SPAN', (7, 3), (7, 4)),
        ('SPAN', (8, 3), (8, 4)),
        ('SPAN', (9, 3), (9, 4)),
        ('SPAN', (2, 3), (5, 3)),
        ('SPAN', (3, 4), (5, 4)),
        ('SPAN', (3, 6), (5, 6)),
        ('SPAN', (3, 7), (5, 7)),
        ('SPAN', (3, 8), (5, 8)),
        ('SPAN', (3, 9), (5, 9)),
        ('SPAN', (4, 3), (5, 3)),
        ('SPAN', (0, 5), (6, 5)),
        ('SPAN', (7, 5), (9, 5)),
        ('SPAN', (0, 6), (1, 6)),
        ('SPAN', (0, 7), (1, 7)),
        ('SPAN', (0, 8), (1, 8)),
        ('SPAN', (0, 9), (1, 9)),
        ('SPAN', (0, 10), (5, 10)),
        ('SPAN', (7, 10), (8, 10)),
    ])

    # формируем таблицу
    table = Table(data)
    table.setStyle(style)

    # формируем документ
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="salary_payment.pdf"'
    buff = BytesIO()
    doc = SimpleDocTemplate(buff, pagesize=landscape(A4))
    
    # задание стиля для заголовка
    title_style = styles['Heading1']
    title_style.fontName = 'Times New Roman Cyr'
    story = [Paragraph('Расчетный лист за ' + str(year) + '-' + str(month), title_style)]
    story.append(table)
    doc.build(story)

    # сохраняем и отправляем файл
    response.write(buff.getvalue())
    buff.close()
    return response

def generate_ndfl(request):
    # получаем данные сотрудника, месяц и год за который нужно произвести расчет
    employee = Employee.objects.get(id=request.GET.get('employee_id'))
    curr_date = request.GET.get('month')
    year = curr_date.split('-')[0]
    month = curr_date.split('-')[1]
    # сформируем дату для корректной работы в виде объекта "дата"
    curr_date = date(int(year), int(month), 1)
    
    # получаем расчетный лист что бы знать оплату за расчетный период
    salary_payment = SalaryPayment.objects.get(employee=employee, year=year, month=month)

    # получаем компанию, она единая но нужна для формирования расчетного листа
    company = Company.objects.get(id=1)

    
    buff = BytesIO()
    # Создаем PDF-документ и указываем размер страницы
    c = canvas.Canvas(buff, pagesize=(595, 842))
    # регистрация кириллического шрифта
    pdfmetrics.registerFont(TTFont('Times New Roman Cyr', 'times.ttf'))
    # Устанавливаем шрифты для документа
    c.setFont('Times New Roman Cyr', 12)

    # Выводим реквизиты компании
    c.drawString(250, 810, "ИНН: {}".format(company.inn))
    c.drawString(250, 790, "КПП: {}".format(company.kpp))
    c.drawString(150, 760, "Справка о доходах и суммах налога физических лиц")
    c.drawString(50, 730, f'Номер справки {random.randint(50, 200)}')
    c.drawString(300, 730, f'Номер корректировки 0')
    c.drawString(50, 690, f'Раздел 1. Данные о физическом лице-получаетеле дохода')
    c.drawString(50, 670, f'ИНН в РФ')
    c.drawString(150, 670, employee.inn)
    c.drawString(50, 650, f'Фамилия')
    c.drawString(150, 650, employee.full_name.split(' ')[0])
    c.drawString(50, 630, f'Имя')
    c.drawString(150, 630, employee.full_name.split(' ')[1])
    c.drawString(50, 610, f'Отчество')
    c.drawString(150, 610, employee.full_name.split(' ')[2])
    c.drawString(50, 590, "Статус налогоплательцика")
    c.drawString(200, 590, "1")
    c.drawString(230, 590, "Дата рождения")
    c.drawString(310, 590, f"{employee.birth_date.day}.{employee.birth_date.month}.{employee.birth_date.year}")
    c.drawString(400, 590, "Гражданство (код страны)")
    c.drawString(550, 590, "630")
    c.drawString(50, 570, "Код вида документа")
    c.drawString(200, 570, "21")
    c.drawString(230, 570, "Серия и номер")
    c.drawString(310, 570, f"{employee.passport}")
    c.drawString(50, 530, "Раздел 2. Общие суммы дохода и налога по итогам налогового периода")
    c.drawString(440, 530, "Ставка налога 13%")
    c.drawString(50, 510, "КБК") # общий для рф
    c.drawString(150, 510, "18210102010011000110") # общий для рф
    c.drawString(50, 490, "Сумма дохода")
    c.drawString(150, 490, f"{salary_payment.total}")
    c.drawString(50, 470, "Сумма налога")
    c.drawString(50, 460, "исчисления")
    c.drawString(150, 470, f"{round(salary_payment.total * Decimal(0.13), 0)}")
    c.drawString(300, 470, "Сумма налога")
    c.drawString(300, 460, "удержания")
    c.drawString(400, 470, f"{round(salary_payment.total * Decimal(0.13), 0)}")
    c.drawString(100, 130, "Достоверность и полноту сведений, указанных на настоящей странице подтверждаю")
    c.drawString(150, 100, "________________")
    c.drawString(250, 100, "(подпись)")
    c.drawString(350, 100, f"{date.today()}")
    c.drawString(420, 100, "(дата)")

    # Сохраняем документ
    c.save()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ndfl_report.pdf"'
    # сохраняем и отправляем файл
    response.write(buff.getvalue())
    buff.close()
    return response
