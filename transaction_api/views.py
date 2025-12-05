from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Transaction
from .serializers import TransactionSerializer

import json

# @api_view(['GET'])
# def get_all_transactions(response):
