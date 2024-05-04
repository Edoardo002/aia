from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .models import UserManager
from .serializers import UserSerializer
from datetime import datetime
from datetime import timedelta

@api_view(['POST'])
@csrf_exempt
def checkAuthentication(request):
    print('Checking...')
    user_id = request.data.get('user_id')
    user_obj = User.objects.get(id=user_id)
    today = datetime.today()
    limit = today - timedelta(hours=4)
    if user_obj.last_login.timestamp() > limit.timestamp():
        return Response({'success': 'okay'}, status=status.HTTP_200_OK)
    else:
        return Response({'session expired'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@csrf_exempt
def login_view(request):
    print('Loggin in...')
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def logout_view(request):
    print('Loggin out...')
    logout(request)
    return Response({'success': 'Logged out successfully'})

@api_view(['POST'])
@csrf_exempt
def signup_view(request):
    print('Signin up...')
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        #serializers.save()
        UserManager.create_user(self=User.objects, email=serializer.validated_data['email'], password=request.data.get('password'), 
                                first_name=serializer.validated_data['first_name'], last_name=serializer.validated_data['last_name']) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)