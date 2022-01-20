from base64 import b64decode
from logging import raiseExceptions
from django.shortcuts import render
from rest_framework.generics import ListAPIView ,CreateAPIView
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.decorators import api_view ,permission_classes
from . import serializers
from . import models
from .decorators import admin_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.decorators import user_passes_test
import jwt





class Login(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.MyTokenObtainPairSerializer

#Admin Views


@permission_classes([IsAuthenticated,])
@api_view(['GET'])
def View_All_Users(request):
    logged_user = models.CustomUser.objects.get(email=request.user.email)
    if logged_user.role=="Admin":
        queryset = models.CustomUser.objects.all()
        response_data = []
        for i in queryset:
            resposne_dict = {}
            resposne_dict['user'] = i.name
            resposne_dict['email'] = i.email
            resposne_dict['role'] = i.role
            response_data.append(resposne_dict)
        return Response(response_data,status=status.HTTP_200_OK)
    else:
        return Response({'message':'For looking into user you must be Admin'},status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def Add_role_to_user(request):
    logged_user = models.CustomUser.objects.get(email=request.user.email)
    if logged_user.role=="Admin":
        request_data = request.data
        user_id = request_data['user_Id']
        role = request_data['role']
        try:
            user = models.CustomUser.objects.get(id=user_id)
            user.role = role
            email = user.email
            user.save()
            return Response({'message':'Role for the user is set now','user_email':email},status=status.HTTP_201_CREATED)
        except raiseExceptions:
            return Response({'message':'User with the given id is not there.'},status=status.HTTP_400_BAD_REQUEST)
     
#user views
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def User_details(request):
    try:
        logged_user = models.CustomUser.objects.get(id=request.user.id)
        param = request.query_params.get('user_Id')
        print(param)
        if logged_user.role=="Admin" and param is not None:
            try:
                user = models.CustomUser.objects.get(id=param)
                response_data = {}
                response_data['name'] = user.name
                response_data['email'] = user.email
                response_data['role'] = user.role
                return Response(response_data,status=status.HTTP_200_OK)
            except:
                return Response({'message':'there is no valid user with this id'},status=status.HTTP_400_BAD_REQUEST)

        else:
            token = str(request.headers['Authorization']).replace('Bearer ',"")
            decode_token = jwt.decode(token,'django-insecure-6xwsq8ps(o3p_y$*v0-3uogoe1=h+pcv2w+u!xkx!+ck60dw0s',algorithms=['HS256'])
            user_id = decode_token['user_id']
            try:
                user = models.CustomUser.objects.get(id=user_id)
                response_data = {}
                response_data['name'] = user.name
                response_data['email'] = user.email
                response_data['role'] = user.role
                return Response(response_data,status=status.HTTP_200_OK)
            except:
                return Response({'message':'there is no valid user with this id'},status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"message":"No User logged in"},status=status.HTTP_400_BAD_REQUEST)

class Register_User(CreateAPIView):
    serializer_class = serializers.UserSerilaizer
    permission_classes = [AllowAny,]  