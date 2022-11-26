from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from . import serializers
from Web import models


@csrf_exempt
def systemDependences(request):
    if request.method == 'GET':
        data = models.System_Dependences.objects.all()
        systemDependencesSer = serializers.System_Dependences_Serializer(data, many=True)
        return JsonResponse(systemDependencesSer.data, safe=False)


# @api_view(['GET', 'POST'])
@csrf_exempt
def accountSettings(request):
    if request.method == 'GET':
        data = models.Account_Setting.objects.all()
        accountSettingSer = serializers.Account_Setting_Serializer(data, many=True)
        return JsonResponse(accountSettingSer.data, safe=False)


@csrf_exempt
def cashTransactions(request):
    if request.method == 'GET':
        data = models.Cash_Transaction.objects.all()
        cashTransactionsSer = serializers.Cash_Transaction_Serializer(data, many=True)
        return JsonResponse(cashTransactionsSer.data, safe=False)
