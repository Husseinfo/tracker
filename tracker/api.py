from base64 import b64decode
from datetime import datetime
from json import loads

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import temp_path
from .models import User, Attendance
from .recognition import predict
from .serializers import AttendanceSerializer


class AttendanceRecord(APIView):
    def post(self, request):
        data = loads(request.body)
        date = datetime.fromtimestamp(int(data['date']))
        inout = data['inout']
        paths = []
        for i, photo in enumerate(data['images']):
            name = f'{temp_path}/rec{i}.png'
            with open(name, 'wb') as fh:
                fh.write(b64decode(photo))
            paths.append(name)

        user_id, percentage = predict(*paths)
        if user_id not in (-1, None) and percentage == 100:
            data_rec = {'user': user_id, 'date': date, 'inout': inout}
            serializer = AttendanceSerializer(data=data_rec)
            if serializer.is_valid():
                # Add DB records
                serializer.save()
                inout = Attendance.objects.last().inout
                # Save captured images for future training
                # utility.add_new_user_photos(user=user_id, path=paths[0])
                user = User.objects.get(id=user_id)
                json_data = {'user': user.first_name + ' ' + user.last_name, 'inout': inout}
                return JsonResponse(json_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
