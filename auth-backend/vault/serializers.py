
from django.contrib.auth.models import User
from pydantic import fields
from rest_framework import serializers

from vault.models import Biometria

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']
        extra_kwargs = {'password':{'write_only':True,'required':True}}
    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email',''),
            password=validated_data['password']
        )
        return user
    def update(self, instance, validated_data):
        password = validated_data.get('password',None)
        for attr, value in validated_data.items():
            setattr(instance,attr,value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class BiometriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biometria
        fields = ['bioId','user','name','embedding']
        extra_kwargs = {
            'name':{'required':False, 'allow_blank':True}
        }

