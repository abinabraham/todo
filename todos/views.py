from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework import status

from django.core.serializers.json import DjangoJSONEncoder
from django.http import (HttpResponse, HttpResponseBadRequest, 
                           HttpResponseForbidden)
from django.http import JsonResponse

from .models import Task
from .serializers import TaskSerializer

class TasksViewSet(ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    json_encoder = DjangoJSONEncoder
    json_content_type = 'application/json;charset=UTF-8'

    def list(self, request):
        serializer = TaskSerializer(self.queryset, many=True)
        # return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse({'data':serializer.data}, status=status.HTTP_200_OK, safe=False)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = TaskSerializer(item)
        # return Response(serializer.data)
        return JsonResponse({'data':serializer.data}, status=status.HTTP_200_OK, safe=False)
      
    def destroy(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        self.perform_destroy(item)
        # return Response(status=status.HTTP_200_OK)
        return JsonResponse({}, status=status.HTTP_200_OK, safe=False)
      
    def perform_destroy(self, instance):
        instance.delete()
        
    def create(self, request):
        serializer = self.get_serializer(data=request.data, context= {'request': self.request})
        if serializer.is_valid():
            self.perform_create(serializer)     
            # return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response({'data':serializer.data}, status=status.HTTP_200_OK)
            return JsonResponse({'data':serializer.data}, safe=False, status=status.HTTP_200_OK)
        else:
            # return Response({'data':serializer.data}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return JsonResponse({'data':serializer.data}, status=status.HTTP_422_UNPROCESSABLE_ENTITY, safe=False)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data':serializer.data}, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'data':serializer.data}, status=status.HTTP_422_UNPROCESSABLE_ENTITY, safe=False)