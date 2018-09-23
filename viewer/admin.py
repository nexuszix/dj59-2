from django.contrib import admin
from .models import RawData, Update, MasterStock
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.
"""
admin.site.register(RawData)
admin.site.register(Update)
"""

class RawResource(resources.ModelResource):
	class Meta:
		model = RawData

@admin.register(RawData)
class RawAdmin(ImportExportModelAdmin):
	resource_class = RawResource
	list_display = ('stock_abbr', 'director', 'stock_type', 'received_date', 'amount', 'price', 'transaction_type',)
# # 	list_filter = ('province',)
	search_fields = ['stock_abbr__stock_abbr']

class UpdateResource(resources.ModelResource):
	class Meta:
		model = Update

@admin.register(Update)
class UpdateAdmin(ImportExportModelAdmin):
	resource_class = UpdateResource
	list_display = ('latest',)
# # 	list_filter = ('province',)
	search_fields = ['latest']		
	
class MasterResource(resources.ModelResource):
	class Meta:
		model = MasterStock

@admin.register(MasterStock)
class MasterAdmin(ImportExportModelAdmin):
	resource_class = MasterResource
	list_display = ('stock_abbr', 'name')
# # 	list_filter = ('province',)
	search_fields = ['stock_abbr', 'name']		


admin.site.site_header = "59-2 Administration System"