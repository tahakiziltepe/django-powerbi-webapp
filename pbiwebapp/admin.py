from django.contrib import admin
from .models import *

# Register your models here.
class CapacityAdmin(admin.ModelAdmin):
    list_display = ['capacityId', 'capacityName', 'insertedDate', 'powerbi_setting']

class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ['workspaceId', 'workspaceName', 'insertedDate', 'capacityId']

class PowerBI_SettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']



admin.site.register(PowerBI_Setting,PowerBI_SettingAdmin)
admin.site.register(Capacity,CapacityAdmin)
admin.site.register(Workspace,WorkspaceAdmin)
admin.site.register(Dataset)

