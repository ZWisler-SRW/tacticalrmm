from django.urls import path

from . import views

urlpatterns = [
    path("<agent:agent_id>/", views.GetWindowsUpdates.as_view()),
    path("<agent:agent_id>/scan/", views.ScanWindowsUpdates.as_view()),
    path("<agent:agent_id>/install/", views.InstallWindowsUpdates.as_view()),
    path("retrieve/", views.RetrieveWindowsUpdates.as_view()),
    path("populate/", views.PopulateWindowsUpdates.as_view()),
    path("all/<str:kb>/", views.EditAllWindowsUpdates.as_view()),
    path("<int:pk>/", views.EditWindowsUpdates.as_view()),
]
