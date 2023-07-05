import random
import string
from decimal import Decimal
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from payrollcalculation.models import Employee, EmploymentContract, Agreement, TimeSheet, Vacation, SickLeave, Violation, Bonus, Company


class Command(BaseCommand):
    help = 'Fill the database with sample data based on Russian legislation'

    def handle(self, *args, **options):

        # Создаем компанию
        inn = ''
        for i in range(10):
            inn += str(random.randint(0, 9))
        inn += str(sum([int(inn[i]) * (10 - i) for i in range(10)]) % 11 % 10)
        inn += str(sum([int(inn[i]) * (11 - i) for i in range(11)]) % 11 % 10)
        company = Company.objects.create(
            name='Агент007',
            inn=inn,
            mrot=16242.00,
            kpp='123456789'
        )

        # Создаем сотрудников
        inn = ''
        for i in range(10):
            inn += str(random.randint(0, 9))
        inn += str(sum([int(inn[i]) * (10 - i) for i in range(10)]) % 11 % 10)
        inn += str(sum([int(inn[i]) * (11 - i) for i in range(11)]) % 11 % 10)
        employee1 = Employee.objects.create(
            full_name='Иванов Иван Иванович',
            inn=inn,
            passport='7100-600154',
            birth_date=date(1997, 8, 1),
            department='Отдел разработки',
            position='Программист'
        )

        inn = ''
        for i in range(10):
            inn += str(random.randint(0, 9))
        inn += str(sum([int(inn[i]) * (10 - i) for i in range(10)]) % 11 % 10)
        inn += str(sum([int(inn[i]) * (11 - i) for i in range(11)]) % 11 % 10)
        employee2 = Employee.objects.create(
            full_name='Петров Петр Петрович',
            inn=inn,
            passport='7120-620154',
            birth_date=date(1997, 8, 2),
            department='Отдел маркетинга',
            position='Дизайнер'
        )

        inn = ''
        for i in range(10):
            inn += str(random.randint(0, 9))
        inn += str(sum([int(inn[i]) * (10 - i) for i in range(10)]) % 11 % 10)
        inn += str(sum([int(inn[i]) * (11 - i) for i in range(11)]) % 11 % 10)
        employee3 = Employee.objects.create(
            full_name='Сидоров Сидор Сидорович',
            inn=inn,
            passport='7133-540154',
            birth_date=date(1998, 6, 1),
            department='Отдел продаж',
            position='Менеджер'
        )

        # Создаем договоры
        contract1 = EmploymentContract.objects.create(
            employee=employee1,
            number='1/2022',
            contract_type='Бессрочный трудовой договор',
            date=date(2022, 1, 1),
            salary_type='fixed',
            salary_rate=Decimal('50000.00'),
            bonus_conditions='доп. нагрузка до 50ч/неделя',
            work_schedule='40ч/неделя',
            start_date=date(2022, 1, 1),
            hiring_conditions='без доп условий'
        )

        contract2 = EmploymentContract.objects.create(
            employee=employee2,
            number='2/2022',
            contract_type='Бессрочный трудовой договор',
            date=date(2022, 1, 1),
            salary_type='hourly',
            salary_rate=Decimal('200.00'),
            bonus_conditions='за месяц отработано на 180%(ч/неделя) от минимума',
            work_schedule='по часам, мин. 25ч/неделя',
            start_date=date(2022, 1, 1),
            hiring_conditions='без доп условий'
        )

        contract3 = EmploymentContract.objects.create(
            employee=employee3,
            number='3/2022',
            contract_type='Бессрочный трудовой договор',
            date=date(2022, 1, 1),
            salary_type='piecework',
            salary_rate=Decimal('120.00'),
            bonus_conditions='продано 150 экземпляров продукта',
            work_schedule='сдельная',
            start_date=date(2022, 1, 1),
            hiring_conditions='без доп условий'
        )

        # Создаем соглашения
        agreement1 = Agreement.objects.create(
            contract=contract1,
            date=date(2022, 4, 1),
            salary_type=contract1.salary_type,
            salary_rate=contract1.salary_rate*Decimal(1.1),
            work_schedule=contract1.work_schedule
        )

        # Создаем записи об учете рабочего времени
        time_sheet1 = TimeSheet.objects.create(
            employee=employee1,
            date=date(2023, 3, 1),
            hours_worked=93.5
        )

        time_sheet2 = TimeSheet.objects.create(
            employee=employee2,
            date=date(2023, 3, 1),
            hours_worked=100
        )

        time_sheet3 = TimeSheet.objects.create(
            employee=employee3,
            date=date(2023, 3, 1),
            piecework_payment=Decimal('500.00')
        )

        # Создаем записи об отпуске
        vacation1 = Vacation.objects.create(
            employee=employee1,
            start_date=date(2023, 3, 1),
            vacation_days=14
        )

        # Создаем записи о больничном
        sick_leave2 = SickLeave.objects.create(
            employee=employee2,
            start_date=date(2023, 3, 1),
            days=6
        )

        # Создаем записи о нарушениях
        violation1 = Violation.objects.create(
            employee=employee1,
            date=date(2023, 3, 24),
            description='опоздал на работу 3 раза в течение недели',
            fine=Decimal(500.0),
        )

        bonus3 = Bonus.objects.create(
            employee=employee3,
            date=date(2023, 3, 1),
            amount=15000,
            description='по условиям договора',
        )