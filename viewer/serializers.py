from rest_framework import serializers
from viewer.models import MasterStock, RawData

class Summary(object):
	def __init__(self, stock_abbr, value, last_cost, avg_cost):
		self.stock_abbr = stock_abbr
		self.amount = value
		self.last_cost = last_cost
		self.avg_cost = avg_cost

class SummarySerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	stock_abbr = serializers.CharField(max_length=8)
	amount = serializers.DecimalField(max_digits=20, decimal_places=2)
	last_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
	avg_cost = serializers.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
		ordering = ('-amount', 'stock_abbr')