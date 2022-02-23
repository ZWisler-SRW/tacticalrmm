from django.urls import path

from . import views

urlpatterns = [
    path("", views.GetAllGroups.as_view()),
    path("create/", views.CreateGroup.as_view()),
    path("edit/<int:id>/", views.EditGroup.as_view()),
    path("delete/<int:id>/", views.DeleteGroup.as_view()),
    path("add/<agent:agent_id>/", views.AddGroupMember.as_view()),
    path("remove/<agent:agent_id>/", views.RemoveGroupMember.as_view()),
]
