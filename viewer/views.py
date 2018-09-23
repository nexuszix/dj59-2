from django.shortcuts import render
from .models import RawData, Update, MasterStock
from .forms import SearchDateForm
import json, requests
from decimal import Decimal
from datetime import datetime, date, timedelta

# Create your views here.
def main(request):
    return render(request, 'viewer/main.html', {})

def render_list(request):
	posts = RawData.objects.all()
	return render(request, 'viewer/listview.html', {'posts': posts})
	
def summary_list(request):
	return render(request, 'viewer/summaryview.html', {'posts': posts, 'latest':latest.latest, 'days': days})

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
			post['doc_date'] = date_convert(post['doc_date'])
			post['received_date'] = date_convert(post['received_date'])
			post['amount'] = Decimal(post['amount'].replace(',',''))
			post['price'] = Decimal(post['price'].replace(',',''))
			company = post.pop('company')
			stock_master = MasterStock.objects.filter(stock_abbr=post['stock_abbr'])
			if not stock_master:
				stock_master = MasterStock(stock_abbr=post['stock_abbr'], name=company)
				stock_master.save()
			else:
				stock_master = stock_master[0]
			post['stock_abbr'] = stock_master
			
			row = RawData(**post)
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


