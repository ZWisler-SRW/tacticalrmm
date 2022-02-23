from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Agent, Groups
from .permissions import GroupsPerms
from .serializers import (GroupSerializer)

class GetAllGroups(APIView):
    permission_classes = [IsAuthenticated, GroupsPerms]

    def get(self, request):
        groups = Groups.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

class CreateGroup(APIView):
    permission_classes = [IsAuthenticated, GroupsPerms]

    def post(self, request):
        obj, created = Groups.objects.get_or_create(name=request.data["name"],
            defaults={
                "name": request.data["name"],
                "status": True
            }
        )
        if created:
            return Response({"status": 1, "message": f"Group: {request.data['name']} was created"})
        else:
            return Response({"status": 0, "message": f"Could not create the group: {request.data['name']}, it already exists"})

class EditGroup(APIView):
    permission_classes = [IsAuthenticated, GroupsPerms]

    def put(self, request, id):
        group = Groups.objects.filter(name=request.data["name"]).first()
        if (group):
            return Response({"status": 0, "message": f"Failed to update group: {request.data['name']}, that group name already exists"})
        else:
            upd = Groups.objects.filter(id=id).update(name=request.data["name"])
            if (upd):
                return Response({"status": 1, "message": f"Group: {request.data['name']} was updated"})
            else:
                return Response({"status": 0, "message": f"Failed to update group: {request.data['name']}"})

class DeleteGroup(APIView):
    permission_classes = [IsAuthenticated, GroupsPerms]

    def delete(self, request, id):
        # Remove the group from any agents that have it assigned
        agents = Agent.objects.filter(groups__contains=[id])
        # Need to find a way to make this more efficent
        for obj in agents:
            obj.groups.remove(id)
            obj.save()

        # Need to remove the group from any roles that have it assigned

        group = Groups.objects.filter(id=id).delete()
        if (group):
            return Response({"status": 1, "message": f"The group was deleted"})
        else:
            return Response({"status": 0, "message": f"Failed to delete the group"})

class AddGroupMember(APIView):
    permission_classes = [IsAuthenticated, GroupsPerms]

    def put(self, request, agent_id):
        obj = Agent.objects.filter(agent_id=agent_id).get()
        if obj.hostname:
            obj.groups.append(request.data["group_id"])
            obj.save()
        return Response({"status": 1, "message": f"Group member added"})

class RemoveGroupMember(APIView):
    permission_classes = [IsAuthenticated, GroupsPerms]

    def put(self, request, agent_id):
        obj = Agent.objects.filter(agent_id=agent_id).get()
        if obj.hostname:
            obj.groups.remove(request.data["group_id"])
            obj.save()
        return Response({"status": 1, "message": f"Group member removed"})
