from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Worker, RawSignings
from settlement.models import Settlement
from datetime import datetime, timezone, timedelta
import pandas as pd
from common.util import normalize_date, get_start_end_week_dates

# Create your views here.
def home(request):
    return render(request, 'workers/home.html')

def upload_signings(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)

        dates = []
        for index, row in df.iterrows():
            if index > 3:
                document = row.iloc[10]
                name = row.iloc[2]
                worker = Worker.objects.filter(document=document).first()
                if not worker:
                    worker = Worker.objects.create(
                        document=document,
                        name=name,
                    )

                date_signed = row.iloc[1].replace(tzinfo=timezone(timedelta(hours=-5)))
                normalized_date_signed = normalize_date(date_signed)
                signed_type="E" if row.iloc[4] == "entrada" else "S"

                if not dates:
                    start_date, end_date = get_start_end_week_dates(normalized_date_signed)
                    dates.append({"start_date": start_date, "end_date": end_date})
                else:
                    found_in_week = False
                    for date_range in dates:
                        if date_range["start_date"] <= normalized_date_signed <= date_range["end_date"]:
                            found_in_week = True
                            break
                    if not found_in_week:
                        start_date, end_date = get_start_end_week_dates(normalized_date_signed)
                        dates.append({"start_date": start_date, "end_date": end_date})

                entry = RawSignings.objects.filter(worker=worker, date_signed=date_signed).first()
                if not entry:
                    RawSignings.objects.create(
                        folder_number=row.iloc[0],
                        date_signed=date_signed,
                        normalized_date_signed=normalized_date_signed,
                        worker=worker,
                        signed_type=signed_type,
                        door=row.iloc[5],
                        contract_number=row.iloc[6],
                    )
        
        for date_range in dates:
            settlement = Settlement.objects.filter(start_date=date_range["start_date"], end_date=date_range["end_date"]).first()
            if not settlement:
                Settlement.objects.create(
                    start_date=date_range["start_date"],
                    end_date=date_range["end_date"],
                )

        return redirect('/settlement/')

    return render(request, 'workers/upload_excel.html')
