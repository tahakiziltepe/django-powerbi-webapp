from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from .models import *
from .utils import *
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test


# Create your views here.


def IndexView(request):
    capacities = Capacity.objects.annotate(workspace_count=Count('workspace'))
    workspaces = Workspace.objects.annotate(dataset_count=Count('dataset')).order_by('-dataset_count')[:5]
    datasets = Dataset.objects.filter(insertedDate__lte=timezone.now()).order_by("-insertedDate")[:5]
    data = {'capacities': capacities,
            'workspaces': workspaces,
            'datasets': datasets,
            }
    return render(request, 'pbiwebapp/index.html', data)


class CapacityView(generic.ListView):
    model = Capacity
    template_name = "pbiwebapp/capacities.html"
    context_object_name = "capacities"

    def get_queryset(self):
        queryset = super().get_queryset()
        annotated_queryset = queryset.annotate(workspace_count=Count('workspace')).order_by('-workspace_count')
        return annotated_queryset


class WorkspaceView(generic.ListView):
    model = Workspace
    template_name = "pbiwebapp/workspaces.html"
    context_object_name = "workspaces"

    def get_queryset(self):
        queryset = super().get_queryset()
        annotated_queryset = queryset.annotate(dataset_count=Count('dataset')).order_by('-dataset_count')
        return annotated_queryset


class DatasetView(generic.ListView):
    paginate_by = 25
    model = Dataset
    template_name = "pbiwebapp/datasets.html"
    context_object_name = "datasets"

    def get_queryset(self):
        queryset = Dataset.objects.filter(insertedDate__lte=timezone.now()).order_by("-insertedDate")
        return queryset


@staff_member_required
def update_capacities(request):
    pbi_settings = PowerBI_Setting.objects.first()
    print(f"1 -- Views -- PBI_SETTINGS ---{pbi_settings}")
    access_token = request_access_token(pbi_settings.app_id,
                                        pbi_settings.tenant_id,
                                        pbi_settings.username,
                                        pbi_settings.password)
    print(f"2 -- Views -- ACCESS TOKEN ---{access_token}")
    func_update_capacities(access_token)
    print(f"3 -- Views -- RUN FUNCTION ---")
    return redirect('pbiwebapp:capacities')


@staff_member_required
def delete_capacity_from_db(request,v_id):
    c = Capacity.objects.filter(id=v_id)
    c.delete()
    return redirect('pbiwebapp:index')


@staff_member_required
def update_workspaces(request):
    pbi_settings = PowerBI_Setting.objects.first()
    print(f"1 -- Views -- PBI_SETTINGS ---{pbi_settings}")
    access_token = request_access_token(pbi_settings.app_id,
                                        pbi_settings.tenant_id,
                                        pbi_settings.username,
                                        pbi_settings.password)
    print(f"2 -- Views -- ACCESS TOKEN ---{access_token}")
    func_update_workspaces(access_token)
    print(f"3 -- Views -- RUN FUNCTION ---")
    return redirect('pbiwebapp:workspaces')


@staff_member_required
def delete_workspace_from_db(request,v_id):
    c = Workspace.objects.filter(id=v_id)
    c.delete()
    return redirect('pbiwebapp:index')


@staff_member_required
def update_datasets(request):
    pbi_settings = PowerBI_Setting.objects.first()
    print(f"1 -- Views -- PBI_SETTINGS ---{pbi_settings}")
    access_token = request_access_token(pbi_settings.app_id,
                                        pbi_settings.tenant_id,
                                        pbi_settings.username,
                                        pbi_settings.password)
    print(f"2 -- Views -- ACCESS TOKEN ---{access_token}")
    func_update_datasets(access_token)
    print(f"3 -- Views -- RUN FUNCTION ---")
    return redirect('pbiwebapp:datasets')



@staff_member_required
def delete_dataset_from_db(request,v_id):
    c = Dataset.objects.filter(id=v_id)
    c.delete()
    return redirect('pbiwebapp:index')


@staff_member_required
def edit_powerbi_setting(request):
    context = {}
    context["pbisettings"] = PowerBI_Setting.objects.first()

    context["capacity_last_refresh"] = Capacity.objects.values('insertedDate').order_by('-insertedDate').first()
    context["workspace_last_refresh"] = Workspace.objects.values('insertedDate').order_by('-insertedDate').first()
    context["dataset_last_refresh"] = Dataset.objects.values('insertedDate').order_by('-insertedDate').first()
    
    context["form"] = add_powerbi_setting_form()
    
    if request.method == "POST":
        pbi_setting_form = add_powerbi_setting_form(request.POST)
        if pbi_setting_form.is_valid():
            obj = PowerBI_Setting(app_id = request.POST['app_id_'],
                                tenant_id = request.POST['tenant_id_'],
                                username = request.POST['mail_address_'],
                                password = request.POST['password_']
                                )
            obj.save()
            return redirect("pbiwebapp:edit_powerbi_setting")

    return render(request, 'pbiwebapp/edit_powerbi_setting.html', context)


@staff_member_required
def delete_pbisetting_from_db(request,v_id):
    c = PowerBI_Setting.objects.filter(id=v_id)
    c.delete()
    messages.success(request,"Deleted.")
    return redirect('pbiwebapp:edit_powerbi_setting')