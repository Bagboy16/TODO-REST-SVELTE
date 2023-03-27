from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from todo.api.serializers import *
from django.contrib.auth.models import User
from todo.models import *

@api_view(['GET', 'POST'])
def user_api_view(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_serializer = UserSerializer(users, many = True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        users_serializer = UserSerializer(data = request.data)
        if users_serializer.is_valid():
            users_serializer.save()
            return Response({'message': 'User has been created'}, status=status.HTTP_201_CREATED)
        return Response(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, user_id = None):
    user = User.objects.filter(id=user_id).first()

    if user:
        if request.method == 'GET':
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
            
        elif request.method == 'PUT':
            user_serializer = UserSerializer(user, data = request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            user.delete()
            return Response({'message': 'User has been deleted'}, status=status.HTTP_200_OK)
    return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def task_api_view(request):
    if request.method == 'GET':
        task = tasks.objects.all()
        task_serializer = TaskSerializer(task, many = True)
        return Response(task_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def task_detail_api_view(request, task_id = None):
    task = tasks.objects.filter(id = task_id).first()
    if task:
        if request.method == 'GET':
            task_serializer = TaskSerializer(task)
            return Response(task_serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            task_serializer = TaskSerializer(task, data=request.data)
            if task_serializer.is_valid():
                task_serializer.save()
                return Response(task_serializer.data, status=status.HTTP_200_OK)
            return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            task.delete()
            return Response({'message':'Task {0} has been deleted'.format(task_id)}, status=status.HTTP_200_OK)
    return Response({'message':'Task {0} not found'.format(task_id)}, status=status.HTTP_400_BAD_REQUEST)
