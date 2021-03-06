from django.db import models

# Create your models here.
		
class MasterStock(models.Model):
	stock_abbr = models.CharField(max_length=8, primary_key=True)
	name = models.CharField(max_length=128)
	
	def __unicode__(self):
		return self.stock_abbr
	
class RawData(models.Model):
	stock_abbr = models.ForeignKey(MasterStock, on_delete=models.CASCADE)
	director = models.CharField(max_length=64, blank=True, null=True)
	relationship = models.CharField(max_length=100, blank=True, null=True)
	stock_type = models.CharField(max_length=64)
	doc_date = models.DateField()
	amount = models.DecimalField(max_digits=20, decimal_places=2)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	transaction_type = models.CharField(max_length=64)
	remark = models.CharField(max_length=256, blank=True, null=True)

	class Meta:
		ordering = ["doc_date"]

	def __unicode__(self):
		return self.stock_abbr + " " + self.transaction_type + amount

class Update(models.Model):
	latest = models.DateField()

	class Meta:
		ordering = ["-latest"]

	def __unicode__(self):
		return self.latest

class UploadErrorLog(models.Model):
	stock_abbr = models.CharField(max_length=256, blank=True, null=True)
	director = models.CharField(max_length=256, blank=True, null=True)
	relationship = models.CharField(max_length=256, blank=True, null=True)
	stock_type = models.CharField(max_length=256, blank=True, null=True)
	doc_date = models.CharField(max_length=256, blank=True, null=True)
	amount = models.CharField(max_length=256, blank=True, null=True)
	price = models.CharField(max_length=256, blank=True, null=True)
	transaction_type = models.CharField(max_length=256, blank=True, null=True)
	remark = models.CharField(max_length=256, blank=True, null=True)

	def __unicode__(self):
		return self.stock_abbr + " " + self.transaction_type + amount