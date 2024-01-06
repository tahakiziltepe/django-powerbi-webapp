import msal
import requests
from .models import *
from django.db.models import Count

def request_access_token(v_app_id,v_tenant_id,v_username,v_password):
    app_id = v_app_id
    tenant_id = v_tenant_id
    authority_url = 'https://login.microsoftonline.com/' + tenant_id
    scopes = ['https://analysis.windows.net/powerbi/api/.default']
    client = msal.PublicClientApplication(app_id, authority=authority_url)
    token_response = client.acquire_token_by_username_password(username=v_username, password=v_password, scopes=scopes)
    if not 'access_token' in token_response:
        raise Exception(token_response['error_description'])
    access_id = token_response.get('access_token')
    return access_id

def func_update_capacities(access_token):
    access_id = access_token
    headers = {'Authorization': f'Bearer ' + access_id}
    endpoint = "https://api.powerbi.com/v1.0/myorg/capacities"
    response = requests.get(endpoint, headers=headers)
    print(response)
    response = response.json()
    response = response['value']
    powerbi_setting_instance = PowerBI_Setting.objects.first()
    for r in response:
        defaults = {
            "powerbi_setting" : powerbi_setting_instance,
            "capacityId" : r['id'],
            "capacityName" : r['displayName'],
            "insertedDate" : timezone.now
        }
        Capacity.objects.update_or_create(capacityId=r['id'],defaults=defaults)

def func_update_workspaces(access_token):
    v_capacities = Capacity.objects.all()
    for v_capacity in v_capacities:
        access_id = access_token
        v_capacityId = v_capacity.capacityId
        headers = {'Authorization': f'Bearer ' + access_id}
        endpoint = f"https://api.powerbi.com/v1.0/myorg/groups?$filter=contains(capacityId,'{v_capacityId}')"
        response = requests.get(endpoint, headers=headers)
        response = response.json()
        response = response['value']
        capacity_instance = Capacity.objects.get(capacityId=v_capacityId)
        for r in response:
            defaults = {
                    "capacityId" : capacity_instance,
                    "workspaceId" : r['id'],
                    "workspaceName" : r['name'],
                    "insertedDate" : timezone.now
                }
            Workspace.objects.update_or_create(workspaceId=r['id'],defaults=defaults)


def func_update_datasets(access_token):
    v_workspaces = Workspace.objects.all()
    for v_workspace in v_workspaces:
        access_id = access_token
        v_workspaceId = v_workspace.workspaceId
        headers = {'Authorization': f'Bearer ' + access_id}
        endpoint = f'https://api.powerbi.com/v1.0/myorg/groups/{v_workspaceId}/datasets'
        response = requests.get(endpoint, headers=headers)
        response = response.json()
        response = response['value']
        workspace_instance = Workspace.objects.get(workspaceId=v_workspaceId)
        for r in response:
            defaults = {
                    "workspaceId" : workspace_instance,
                    "datasetId" : r['id'],
                    "datasetName" : r['name'],
                    "insertedDate" : timezone.now
                }
            Dataset.objects.update_or_create(datasetId=r['id'],defaults=defaults)