from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from common.util import get_hours_difference

class Settlement(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    processed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.start_date} - {self.end_date}'

class SettlementDetails(models.Model):
    def working_shifts_default():
        return {
            "monday": None,
            "tuesday": None,
            "wednesday": None,
            "thursday": None,
            "friday": None,
            "saturday": None,
            "sunday": None,
        }

    settlement = models.ForeignKey(Settlement, on_delete=models.CASCADE)
    worker = models.ForeignKey("workers.Worker", on_delete=models.CASCADE)
    monday = models.FloatField(default=0.0)
    tuesday = models.FloatField(default=0.0)
    wednesday = models.FloatField(default=0.0)
    thursday = models.FloatField(default=0.0)
    friday = models.FloatField(default=0.0)
    saturday = models.FloatField(default=0.0)
    sunday = models.FloatField(default=0.0)
    ordinary_hours = models.FloatField(default=0.0)
    daytime_overtime = models.FloatField(default=0.0)
    night_surcharge_hours = models.FloatField(default=0.0)
    night_overtime = models.FloatField(default=0.0)
    holiday_hours = models.FloatField(default=0.0)
    night_holiday_hours = models.FloatField(default=0.0)
    daytime_holiday_overtime = models.FloatField(default=0.0)
    night_holiday_overtime = models.FloatField(default=0.0)
    working_shifts = models.JSONField(encoder=DjangoJSONEncoder, default=working_shifts_default)

    def classify_hours(self, start_date: datetime, end_date: datetime):
        MORNING = 0
        AFTERNOON = 1
        EVENING = 2
        print(f'TURN STARTED AT {start_date} AND FINISHED AT {end_date}')
        if start_date.hour < 10:
            time_of_day = MORNING
        elif 10 <= start_date.hour < 17:
            time_of_day = AFTERNOON
        elif start_date.hour >= 17:
            time_of_day = EVENING

        total_hours = get_hours_difference(start_date, end_date)
        is_holiday = True if start_date.weekday() == 6 else False
        if time_of_day == MORNING:
            remaining_hours = total_hours-8
            ordinary_hours = 8 if remaining_hours > 0 else total_hours
            daytime_overtime = remaining_hours if remaining_hours > 0 else 0
            if is_holiday:
                self.holiday_hours += ordinary_hours
                self.daytime_holiday_overtime += daytime_overtime
            else:
                self.ordinary_hours += ordinary_hours
                self.daytime_overtime += daytime_overtime
            print(f'HO: {self.ordinary_hours} | HED: {self.daytime_overtime} | HF: {self.holiday_hours} | HEFD: {self.daytime_holiday_overtime}')
        elif time_of_day == AFTERNOON:
            pass
        elif time_of_day == EVENING:
            nine_hour = start_date.replace(hour=21, minute=0)
            # Hours till 9 pm
            ordinary_hours = get_hours_difference(start_date, nine_hour)
            remaining_hours = total_hours - ordinary_hours
            ordinary_hours = ordinary_hours if remaining_hours > 0 else total_hours
            if is_holiday:
                self.holiday_hours += ordinary_hours
            else:
                self.ordinary_hours += ordinary_hours
            if remaining_hours > 0:
                # Hours till midnight (eating time between 9 and 10 pm not included)
                night_surcharge_hours = 2 if remaining_hours >= 2 else remaining_hours
                if is_holiday:
                    self.night_holiday_hours += night_surcharge_hours
                else:
                    self.night_surcharge_hours += night_surcharge_hours
                ordinary_hours += night_surcharge_hours
                remaining_hours -= night_surcharge_hours
                remaining_hours -= 1
                if remaining_hours > 0:
                    is_overtime = False
                    overtime_hours = 0.0
                    is_holiday = True if end_date.weekday() == 6 else False
                    night_hours = 0.0
                    print(remaining_hours)
                    while remaining_hours > 0:
                        if ordinary_hours == 8.0 and not is_overtime:
                            is_overtime = True
                        if is_overtime:
                            overtime_hours += 0.5
                        else:
                            ordinary_hours += 0.5
                            night_hours += 0.5
                        remaining_hours -= 0.5

                    if is_holiday:
                        self.night_holiday_hours += night_hours
                        self.night_holiday_overtime += overtime_hours
                    else:
                        self.night_surcharge_hours += night_hours
                        self.night_overtime += overtime_hours

            print(f'HO: {self.ordinary_hours} | HRN: {self.night_surcharge_hours} | HEN: {self.night_overtime} | HF: {self.holiday_hours} | HFN: {self.night_holiday_hours} | HEFN: {self.night_holiday_overtime}')

    def classify_week(self):
        pass
