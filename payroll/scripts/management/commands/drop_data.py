from django.core.management.base import BaseCommand
from payrollcalculation.models import Employee, EmploymentContract, Agreement, TimeSheet, Vacation, SickLeave, Violation, Bonus, Company

# Удаляем все объекты из каждой модели
class Command(BaseCommand):
    help = 'Deletes all data from the all models'

    def handle(self, *args, **options):
        Employee.objects.all().delete()
        EmploymentContract.objects.all().delete()
        Agreement.objects.all().delete()
        TimeSheet.objects.all().delete()
        Vacation.objects.all().delete()
        SickLeave.objects.all().delete()
        Violation.objects.all().delete()
        Bonus.objects.all().delete()
        Company.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all data'))
