"""
Provides tasks to Celery
"""
from __future__ import absolute_import, unicode_literals
from datetime import datetime
from celery import shared_task
from Appointment.models import Meet
from User.models import Doctors


@shared_task
def report_generator():
    """Celery task to create Doctor reports"""
    with open("User/Sorted Doctors.txt", 'w', encoding='utf-8') as report_file:
        report_file.write('\nUpdated Ratings List at: '+str(datetime.now()))
        report_file.write('\n')
    average_ratings_dict = {}
    doctors_id = Doctors.objects.all().values_list('id', flat=True)
    for i in doctors_id:
        doctors_name = Doctors.objects.filter(id=i).values_list('name',
                                                                flat=True)
        assigned_doctor = Meet.objects.filter(assigned_doctor=i).values_list(
                                                                    'rating',
                                                                    flat=True)
        meets = []
        for element in assigned_doctor:
            meets.append(int(element))
        if len(meets) == 0:
            doctor_rating = 0
        else:
            doctor_rating = sum(meets)/len(meets)
        average_ratings_dict[doctors_name[0]] = doctor_rating

    sorted_ratings = sorted(average_ratings_dict.items(), key=lambda x: x[1])
    for line in sorted_ratings:
        with open("User/Sorted Doctors.txt", 'a', encoding='utf-8') as report_file:
            report_file.write(str(line))
            report_file.write('\n')
