
from django.db import models
from django.utils import timezone

# Create your models here.

class PowerBI_Setting(models.Model):
    app_id = models.CharField(max_length = 200)
    tenant_id = models.CharField(max_length = 200)
    username = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    insertedDate = models.DateTimeField("Created at:", default = timezone.now())

    def __str__(self):
        return self.username


class Capacity(models.Model):
    powerbi_setting = models.ForeignKey(PowerBI_Setting, on_delete=models.CASCADE)
    capacityId = models.CharField(max_length = 200)
    capacityName = models.CharField(max_length = 200)
    insertedDate = models.DateTimeField("Created at:" , default = timezone.now())

    def __str__(self):
        return self.capacityId


class Workspace(models.Model):
    capacityId = models.ForeignKey(Capacity, on_delete=models.CASCADE)
    workspaceId = models.CharField(max_length = 200)
    workspaceName = models.CharField(max_length = 200)
    insertedDate = models.DateTimeField("Created at:" , default = timezone.now())

    def __str__(self):
        return self.workspaceId


class Dataset(models.Model):
    workspaceId = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    datasetId = models.CharField(max_length = 200)
    datasetName = models.CharField(max_length = 200)
    insertedDate = models.DateTimeField("Created at:" , default = timezone.now())

    def __str__(self):
        return self.datasetId