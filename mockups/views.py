from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Mockup
from .tasks import generate_mockup

class MockupView(APIView):
    def post(self, request):
        image = request.FILES.get('image')
        text = request.data.get('text')

        if not image or not text:
            return Response({'error': 'image and text required'}, status=400)

        mockup = Mockup.objects.create(image=image, text=text)
        generate_mockup.delay(mockup.id)

        return Response({'message': 'Mockup is being generated', 'id': mockup.id}, status=202)
    
#==============
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import generate_mockup

class MockupGenerateView(APIView):
    def post(self, request):
        text = request.data.get('text')
        font = request.data.get('font', 'arial')
        text_color = request.data.get('text_color', '#000000')
        shirt_colors = request.data.get('shirt_color', ['white', 'black', 'blue', 'red'])

        if not text:
            return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)

        task = generate_mockup.delay(text, font, text_color, shirt_colors)
        return Response({
            "task_id": task.id,
            "status": "PENDING",
            "message": "ساخت تصویر آغاز شد"
        })
# =======================
from celery.result import AsyncResult
from django.conf import settings
from .models import Mockup
from .serializers import MockupSerializer

class TaskStatusView(APIView):
    def get(self, request, task_id):
        task_result = AsyncResult(task_id)
        status = task_result.status

        response_data = {
            "task_id": task_id,
            "status": status,
            "results": []
        }

        if status == "SUCCESS":
            # نتایج تسک (عکس‌ها) رو از دیتابیس بگیریم
            mockups = Mockup.objects.all().order_by('-created_at')[:4]
            serializer = MockupSerializer(mockups, many=True)
            response_data["results"] = serializer.data

        return Response(response_data)


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import MockupSerializer
# from .tasks import generate_mockup

# class GenerateMockupView(APIView):
#     def post(self, request):
#         serializer = MockupSerializer(data=request.data)
#         if serializer.is_valid():
#             text = serializer.validated_data['text']
#             task = generate_mockup.delay(text)
#             return Response({
#                 "message": "Task started",
#                 "task_id": task.id
#             }, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
