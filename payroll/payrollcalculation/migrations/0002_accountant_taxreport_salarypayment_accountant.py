# Generated by Django 4.1.7 on 2023-04-02 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payrollcalculation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accountant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='ФИО')),
            ],
            options={
                'verbose_name': 'Бухгалтер',
                'verbose_name_plural': 'Бухгалтера',
            },
        ),
        migrations.CreateModel(
            name='TaxReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('correction_number', models.CharField(max_length=10)),
                ('accountant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payrollcalculation.accountant')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payrollcalculation.employee')),
            ],
        ),
        migrations.AddField(
            model_name='salarypayment',
            name='accountant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payrollcalculation.accountant'),
        ),
    ]
