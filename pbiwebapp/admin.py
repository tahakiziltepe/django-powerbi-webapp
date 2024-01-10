from django.contrib import admin
from .models import *

# Register your models here.
class CapacityAdmin(admin.ModelAdmin):
    list_display = ['id','capacityId', 'capacityName', 'insertedDate', 'powerbi_setting']

class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ['id','workspaceId', 'workspaceName', 'insertedDate', 'capacityId']

class DatasetAdmin(admin.ModelAdmin):
    list_display = ['id','datasetId', 'datasetName', 'insertedDate', 'workspaceId']

class PowerBI_SettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']



admin.site.register(PowerBI_Setting,PowerBI_SettingAdmin)
admin.site.register(Capacity,CapacityAdmin)
admin.site.register(Workspace,WorkspaceAdmin)
admin.site.register(Dataset,DatasetAdmin)

