from rest_framework import serializers
from Appointment.models import Meet


class MeetSerializer(serializers.ModelSerializer):
    assigned_doctor = serializers.StringRelatedField()

    class Meta:
        model = Meet
        fields = ["patient_id", "start_datetime", "end_datetime", "service", "assigned_doctor", "rating"]
