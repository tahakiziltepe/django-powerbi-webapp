from django.urls import path
from . import views


app_name = "pbiwebapp"
urlpatterns = [
    path('', views.IndexView, name="index"),
    path('workpaces/', views.WorkspaceView.as_view(), name="workspaces"),
    path('datasets/', views.DatasetView.as_view(), name="datasets"),
    path('update_capacities/', views.update_capacities, name="update_capacities"),
    path('update_workspaces/', views.update_workspaces, name="update_workspaces"),
    path('update_datasets/', views.update_datasets, name="update_datasets"),
    path('delete_capacity_from_db/<int:v_id>', views.delete_capacity_from_db, name="delete_capacity_from_db"),
    path('delete_workspace_from_db/<int:v_id>', views.delete_workspace_from_db, name="delete_workspace_from_db"),
    path('delete_dataset_from_db/<int:v_id>', views.delete_dataset_from_db, name="delete_dataset_from_db"),
]