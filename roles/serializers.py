
from rest_framework import serializers
from . import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.email
        token['user_role'] = user.role
        return token
    
    def validate(self,attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        user_model = get_user_model()
        obj = user_model.objects.get(email = self.user.email)
        name = obj.first_name + obj.last_name
        data.update({'user': self.user.email})
        data.update({'name': obj.name})
        return data



class UserSerilaizer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    role = serializers.CharField(source='get_role_display',required=False)


    class Meta:
        model = models.CustomUser
        fields = ('email','name','password','role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
