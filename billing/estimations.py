from django.shortcuts import render, redirect
from .models import Invoice, Estimation, InvoiceBills
from django.http import HttpResponse, JsonResponse
import secrets
from django.db.models import Case, Value, When, Count, Sum

from .forms import CreateInvoice
from random import randint
from num2words import num2words
import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

def Estimations(request):
	if request.method == "GET":
		est = Estimation.objects.all()
		return render(request, 'estimation/estimation.html', {'estimations':est})

def CreateEstimations(request, pk):
	if request.method == 'POST':
		ammount = 0
		invoices = InvoiceBills.objects.filter(invoice=pk).values('totalammount')
		for m in invoices:
			ammount += int(m['totalammount'])
		customer_name = request.POST['customer_name']
		contact = request.POST['contact']
		url = '/'
		Estimation.objects.create(estimation_number=pk, ammount=ammount, costumer_name=customer_name, contact_number=contact)
		return redirect(url)
	else:
		ammount = 0
		invoices = InvoiceBills.objects.filter(invoice=pk).values('totalammount')
		for m in invoices:
			ammount += int(m['totalammount'])
		return render(request, 'estimation/createestimation.html', {'sum':ammount})

def deleteEstimation(request, pk):
	est = Estimation.objects.get(estimation_number=pk)
	est.delete()
	url = '/estimations/'
	return redirect(url)