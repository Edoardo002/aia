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
from . import constants
from bson.json_util import dumps
from pymongo import MongoClient
import secrets

AIP_DB = constants.AIPDB
clientAipDb = MongoClient(host=AIP_DB, port=27017)

@api_view(['POST'])
@csrf_exempt
def checkAuthentication(request):
    print('Checking...')
    user_id = request.data.get('user_id')
    token = request.data.get('token')
    today = datetime.today()
    limit = today - timedelta(hours=4)
    if User.objects.filter(id=user_id).first()==None:
        return Response({'page not reachable'}, status=status.HTTP_401_UNAUTHORIZED)
    user_obj = User.objects.get(id=user_id)
    if user_obj.get_session_auth_hash() != token:
        if User.objects.filter(id=user_id, token=token).exists()==True:
            if user_obj.last_login.timestamp() > limit.timestamp():
                return Response({'success': 'okay'}, status=status.HTTP_200_OK)
            else:
                return Response({'session expired'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'page not reachable'}, status=status.HTTP_401_UNAUTHORIZED)
    if user_obj.last_login is None:
        return Response({'okay'}, status=status.HTTP_200_OK)
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
        return Response({ 'token' : user.get_session_auth_hash(), 'user' : serializer.data })
    else:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@csrf_exempt
def login_ext_view(request):
    print('External log in...')
    email = request.data.get('email')
    aip_db = clientAipDb.get_database("AIP_DB")
    aip_collection = aip_db.get_collection("chatbot_user")
    serializer = UserSerializer(data=request.data)
    if aip_collection.count_documents({ "email": email }) == 0:
        if serializer.is_valid():
            #serializers.save()
            UserManager.create_user(self=User.objects, email=serializer.validated_data['email'], password="ext", last_login=datetime.today(),
                                    first_name=serializer.validated_data['first_name'], last_name=serializer.validated_data['last_name'])
            user = aip_collection.find_one({ "email" : email })
            return Response(dumps(user), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        res = aip_collection.find_one({ "email" : email })
        today = datetime.today()
        limit = today - timedelta(hours=4)
        if res["last_login"].timestamp() < limit.timestamp():
            aip_collection.update_one({ "email" : email }, { "$set": { "last_login": datetime.today(), "token": secrets.token_urlsafe(64) } })
            res = aip_collection.find_one({ "email" : email })
        return Response(dumps(res), status=status.HTTP_200_OK)

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