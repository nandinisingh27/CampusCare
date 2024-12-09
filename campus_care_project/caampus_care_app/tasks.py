# tasks.py

from celery import shared_task
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from .models import Dropdown
def add_working_hours(start_time, target_hours=8):
    current_time = make_aware(datetime.now()) 
    hours_passed = 0

    while hours_passed < target_hours:
        if 9 <= current_time.hour < 17: 
            hours_passed += 1
        current_time += timedelta(hours=1) 
    return current_time

@shared_task
def increase_variable_after_working_hours(data_id):
    data_obj = Dropdown.objects.get(id=data_id)

    future_time = add_working_hours(data_obj.created_at)

    if make_aware(datetime.now()) >= future_time:
        data_obj.data_value += 1
        data_obj.save()
        return f"Variable updated to {data_obj.data_value} after 8 working hours"
    else:
        return "Not enough time has passed yet."
