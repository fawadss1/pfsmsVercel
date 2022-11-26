from rest_framework import serializers
from Web import models


class System_Dependences_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.System_Dependences
        # fields = ('Name', 'Father_Name')
        fields = '__all__'


class Account_Setting_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account_Setting
        # fields = ('Name', 'Father_Name')
        fields = '__all__'


class Cash_Transaction_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cash_Transaction
        # fields = ('Name', 'Father_Name')
        fields = '__all__'
