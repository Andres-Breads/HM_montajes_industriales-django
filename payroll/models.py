from django.db import models
from settlement.models import Settlement, SettlementDetails
from workers.models import Worker

class Payroll(models.Model):
    payroll_date = models.DateField()
    settlement = models.ManyToManyField(Settlement, related_name='payroll')

class PayrollDetail(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='details')
    settlement_detail = models.ManyToManyField(SettlementDetails)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    total_hours = models.FloatField(default=0.0)
    ordinary_hours = models.FloatField(default=0.0)
    daytime_overtime = models.FloatField(default=0.0)
    night_surcharge_hours = models.FloatField(default=0.0)
    night_overtime = models.FloatField(default=0.0)
    holiday_hours = models.FloatField(default=0.0)
    night_holiday_hours = models.FloatField(default=0.0)
    daytime_holiday_overtime = models.FloatField(default=0.0)
    night_holiday_overtime = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return f'HO: {self.ordinary_hours} | HED: {self.daytime_overtime} | HRN: {self.night_surcharge_hours} | HEN: {self.night_overtime} | HF: {self.holiday_hours} | HFN: {self.night_holiday_hours} | HEFD: {self.daytime_holiday_overtime} | HEFN: {self.night_holiday_overtime}'
