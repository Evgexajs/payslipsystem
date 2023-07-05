from datetime import timedelta
from django.db import models

class Employee(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    passport = models.CharField(max_length=20, verbose_name='Паспорт')
    birth_date = models.DateField()
    department = models.CharField(max_length=20, verbose_name='Подразделение')
    position = models.CharField(max_length=20, verbose_name='Должность')
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

class Accountant(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='ФИО')

    class Meta:
        verbose_name = 'Бухгалтер'
        verbose_name_plural = 'Бухгалтера'

class EmploymentContract(models.Model):
    """
    Модель, описывающая договор между компанией и сотрудником.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    number = models.CharField(max_length=12, verbose_name='Номер договора')
    contract_type = models.CharField(max_length=255, verbose_name='Тип договора')
    date = models.DateField(verbose_name='Дата заключения соглашения')
    SALARY_TYPE_CHOICES = (
        ('fixed', 'Фиксированный оклад'),
        ('hourly', 'Почасовая оплата'),
        ('piecework', 'Сдельная оплата')
    )
    salary_type = models.CharField(max_length=10, choices=SALARY_TYPE_CHOICES, verbose_name='Тип заработной платы')
    salary_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Размер оклада или ставки')
    bonus_conditions = models.CharField(max_length=255, verbose_name='Условия начисления дополнительных выплат')
    work_schedule = models.CharField(max_length=255, verbose_name='Режим работы и график работы')
    start_date = models.DateField(verbose_name='Дата начала работы')
    end_date = models.DateField(verbose_name='Дата окончания работы', null=True, blank=True)
    hiring_conditions = models.CharField(max_length=255, verbose_name='Условия приема на работу и увольнения')
    
    class Meta:
        verbose_name = 'Договор о найме'
        verbose_name_plural = 'Договоры о найме'


class Agreement(models.Model):
    contract = models.ForeignKey(EmploymentContract, on_delete=models.CASCADE, verbose_name='Договор')
    date = models.DateField(verbose_name='Дата заключения соглашения')
    SALARY_TYPE_CHOICES = (
        ('fixed', 'Фиксированный оклад'),
        ('hourly', 'Почасовая оплата'),
        ('piecework', 'Сдельная оплата')
    )
    salary_type = models.CharField(max_length=10, choices=SALARY_TYPE_CHOICES, verbose_name='Тип заработной платы')
    salary_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ставка заработной платы')
    work_schedule = models.CharField(max_length=100, verbose_name='График работы')

    class Meta:
        verbose_name = 'Соглашение'
        verbose_name_plural = 'Соглашения'

class TimeSheet(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    date = models.DateField(verbose_name='Дата')
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Отработано часов', blank=True, null=True)
    piecework_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Оплата за сдельную работу', blank=True, null=True)

    class Meta:
        verbose_name = 'Учет рабочего времени'
        verbose_name_plural = 'Учет рабочего времени'

class Vacation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    start_date = models.DateField(verbose_name='Дата начала отпуска')
    end_date = models.DateField(verbose_name='Дата окончания отпуска', blank=True, null=True)
    vacation_days = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Количество отпускных дней')

    class Meta:
        verbose_name = 'Отпуск'
        verbose_name_plural = 'Отпуска'

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=int(self.vacation_days))
        super().save(*args, **kwargs)

class SickLeave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    start_date = models.DateField(verbose_name='Дата начала больничного')
    end_date = models.DateField(verbose_name='Дата окончания больничного', blank=True, null=True)
    days = models.PositiveIntegerField(verbose_name='Количество дней', default=0)
    medical_certificate = models.FileField(verbose_name='Медицинская справка', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.end_date is None:
            self.end_date = self.start_date + timedelta(days=self.days)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Больничный лист'
        verbose_name_plural = 'Больничные листы'

class Violation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    date = models.DateField(verbose_name='Дата нарушения')
    description = models.TextField(verbose_name='Описание нарушения')
    fine = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Штраф', blank=True, null=True)

    class Meta:
        verbose_name = 'Нарушение'
        verbose_name_plural = 'Нарушения'

class Bonus(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    date = models.DateField(verbose_name='Дата начисления')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    description = models.CharField(max_length=255, verbose_name='Описание')

    class Meta:
        verbose_name = 'Премия'
        verbose_name_plural = 'Премии'

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название компании')
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, verbose_name='КПП')
    mrot = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компания'


class SalaryPayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    accountant = models.ForeignKey(Accountant, on_delete=models.CASCADE, null=True, blank=True)
    SALARY_TYPE_CHOICES = (
        ('fixed', 'Фиксированный оклад'),
        ('hourly', 'Почасовая оплата'),
        ('piecework', 'Сдельная оплата')
    )
    salary_type = models.CharField(max_length=10, choices=SALARY_TYPE_CHOICES, verbose_name='Тип заработной платы')
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    worked_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    vacation_allowance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sick_leave_allowance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.employee} - {self.amount} ({self.year}-{self.month})"
    
class TaxReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    accountant = models.ForeignKey(Accountant, on_delete=models.CASCADE)
    date = models.DateField()
    correction_number = models.CharField(max_length=10)
