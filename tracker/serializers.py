from rest_framework import serializers

from tracker.models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('id', 'user', 'date', 'inout')
