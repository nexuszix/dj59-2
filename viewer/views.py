from django.shortcuts import render
from .models import *
from .forms import SearchDateForm
import json, requests
from decimal import Decimal
from datetime import datetime, date, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SummarySerializer, Summary

# Create your views here.
def main(request):
	return render(request, 'viewer/summaryview.html', {})

def render_list(request):
	posts = RawData.objects.all()
	return render(request, 'viewer/listview.html', {'posts': posts})
	
def summary_get(request, pk):
	masters = MasterStock.objects.all()
	posts = []
	##days = request.POST.get("days",90)
	#days = int(days)
	days = int(pk)
	for stock in masters:
		post = {}
		post['stock_abbr'] = stock.stock_abbr
		post['value'] = 0
		volumn = 0
		n = 0
		latest_price = 0
		datas = RawData.objects.filter(stock_abbr__stock_abbr=stock.stock_abbr, doc_date__gte=date.today()-timedelta(days=days))
		if not datas: continue
		for data in datas:
			volumn += data.amount
			n += 1
			latest_price = data.price
			if data.transaction_type == "ซื้อ":
				post['value'] += data.amount * data.price
			elif data.transaction_type == "ขาย":
				post['value'] -= data.amount * data.price
		post['last_cost'] = latest_price
		post['value'] = round(post['value'], 0)
		if volumn > 0:
			post['avg_cost'] = round(post['value']/volumn, 2)
		posts.append(post.copy())
	posts = sorted(posts, key=lambda k: k['value'], reverse=True) 
	return posts

def summary_list(request, pk=90):
	latest = Update.objects.all()[0].latest	
	return render(request, 'viewer/summaryview.html', {'posts': summary_get(request, pk), 'latest':latest, 'days': pk})

def upload(request):
	if request.method == "POST":
		#start_date = request.POST.get("start_date","")
		latest = Update.objects.all()[0]
		start_date = latest.latest + timedelta(days=1)
		end_date = request.POST.get("end_date","")
		end_date = datetime.strptime(end_date, "%Y-%m-%d")
		
		sdd = str(start_date.day).zfill(2)
		smm = str(start_date.month).zfill(2)
		syy = str(start_date.year)
		"""
		sdd = start_date[8:]
		smm = start_date[5:7]
		syy = start_date[:4]
		
		edd = end_date[8:]
		emm = end_date[5:7]
		eyy = end_date[:4]
		"""
		edd = str(end_date.day).zfill(2)
		emm = str(end_date.month).zfill(2)
		eyy = str(end_date.year)
		data = {
			'sdd': sdd,
			'smm': smm,
			'syy': syy,
			'edd': edd,
			'emm': emm,
			'eyy': eyy,
		}
		r = requests.get("http://127.0.0.1:1880/load", params=data)
		posts = json.loads(r.text)
		for post in posts:
			if post['transaction_type'] not in ["ซื้อ", "ขาย"]: continue
			try:
				company = post.pop('company')
				stock_master = MasterStock.objects.filter(stock_abbr=post['stock_abbr'])
				if not stock_master:
					stock_master = MasterStock(stock_abbr=post['stock_abbr'], name=company)
					stock_master.save()
				else:
					stock_master = stock_master[0]
				post['stock_abbr'] = stock_master
				if len(post['relationship']) > 100: post['relationship']=post['relationship'][:100]
				if len(post['stock_type'])>64: post['stock_type']=post['stock_type'][:64]
				post['doc_date'] = date_convert(post['doc_date'])
				post['amount'] = Decimal(post['amount'].replace(',',''))
				post['price'] = Decimal(post['price'].replace(',',''))
				
				row = RawData(**post)
				row.save()
			except:
				row = UploadErrorLog(**post)
				row.save()
		latest = Update.objects.all()[0]
		latest.latest = end_date
		latest.save()

		return render(request, 'viewer/listview.html', {'posts': posts, 'latest':latest.latest, 'url':r.url,})
	else:
		form = SearchDateForm()
		return render(request, 'viewer/upload.html', {'form': form})

def download_list(request):
	pass

def date_convert(dateinput):
	yearoutput = int(dateinput[6:]) - 543
	monthoutput = int(dateinput[3:5])
	dayoutput = int(dateinput[:2])
	return date(yearoutput, monthoutput, dayoutput)

# REST API#
@csrf_exempt 
@api_view(['GET', 'POST'])
def summary_by_date_api(request, pk=90, format=None):
	#posts = summary_list(request)
	posts = []
	summarys=summary_get(request, pk)
	if not summarys:
		return Response(status=status.HTTP_204_NO_CONTENT)
	for row in summarys:
		post = Summary(**row)
		posts.append(post)

	#posts = {'stock_abbr':"TEST", 'amount':1, 'last_cost':2, 'avg_cost':3,}
	serializer = SummarySerializer(posts, many=True)
	return Response(serializer.data)
