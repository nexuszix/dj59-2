from django.db import models

# Create your models here.
class RawData(models.Model):
	stock_abbr = models.CharField(max_length=5)
	company = models.CharField(max_length=128)
	director = models.CharField(max_length=64, blank=True, null=True)
	relationship = models.CharField(max_length=20, blank=True, null=True)
	stock_type = models.CharField(max_length=64)
	doc_date = models.DateField()
	received_date = models.DateField()
	amount = models.DecimalField(max_digits=20, decimal_places=2)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	transaction_type = models.CharField(max_length=64)
	remark = models.CharField(max_length=128, blank=True, null=True)

	class Meta:
		ordering = ["received_date"]

	def __unicode__(self):
		return self.stock_abbr + " " + self.transaction_type + amount

class Update(models.Model):
	latest = models.DateField()

	class Meta:
		ordering = ["-latest"]

	def __unicode__(self):
		return self.latest