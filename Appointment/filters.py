from django_filters.rest_framework import FilterSet
from Appointment.models import Meet


class MeetFilter(FilterSet):
    class Meta:
        model = Meet
        fields = {
            'booked': ['lt', 'gt'],
            'service': ['exact'],
            'rating': ['gt', 'lt']
        }
