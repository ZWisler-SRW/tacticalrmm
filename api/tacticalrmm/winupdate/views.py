import asyncio

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from agents.models import Agent
from tacticalrmm.utils import get_default_timezone
from tacticalrmm.permissions import _has_perm_on_agent

from .models import WinUpdate
from .models import WinUpdateManager
from .permissions import AgentWinUpdatePerms
from django.core import serializers
from .serializers import WinUpdateSerializer, WinUpdateManagerSerializer


class GetWindowsUpdates(APIView):
    permission_classes = [IsAuthenticated, AgentWinUpdatePerms]

    # list windows updates on agent
    def get(self, request, agent_id):
        agent = get_object_or_404(Agent, agent_id=agent_id)
        updates = WinUpdate.objects.filter(agent=agent).order_by("-id", "installed")
        ctx = {"default_tz": get_default_timezone()}
        serializer = WinUpdateSerializer(updates, many=True, context=ctx)
        return Response(serializer.data)

class RetrieveWindowsUpdates(APIView):
    permission_classes = [IsAuthenticated, AgentWinUpdatePerms]

    # list all windows updates that are pending
    def get(self, request):
        updates = WinUpdateManager.objects.all().order_by("-severity", "-kb")
        ctx = {"agents_pending": 0, "agents_installed": 0}
        serializer = WinUpdateManagerSerializer(updates, many=True, context=ctx)
        return Response(serializer.data)

class PopulateWindowsUpdates(APIView):
    permission_classes = [IsAuthenticated, AgentWinUpdatePerms]

    # populate the windows update manager table to include the KB and report against it
    def patch(self, request):
        updates = WinUpdate.objects.all()

        for winupd in serializers.serialize("python", WinUpdate.objects.all()):
            obj,created = WinUpdateManager.objects.update_or_create(kb=winupd["fields"]["kb"],
                defaults={
                    "kb": winupd["fields"]["kb"], 
                    "name": winupd["fields"]["title"],
                    "guid": winupd["fields"]["guid"],
                    "status": winupd["fields"]["action"],
                    "severity": winupd["fields"]["severity"]
                }
            )
            
        return Response(f"Windows updates populated for the Update Manager")

class EditAllWindowsUpdates(APIView):
    permission_classes = [IsAuthenticated, AgentWinUpdatePerms]

    # change approval status of update
    def put(self, request, kb):
        action = request.data["action"]
        WinUpdate.objects.filter(kb=kb).update(action=action)
        return Response(f"Windows update {kb} was changed to {action}")

class ScanWindowsUpdates(APIView):
    permission_classes = [IsAuthenticated, AgentWinUpdatePerms]
    # scan for windows updates on agent
    def post(self, request, agent_id):
        agent = get_object_or_404(Agent, agent_id=agent_id)
        agent.delete_superseded_updates()
        asyncio.run(agent.nats_cmd({"func": "getwinupdates"}, wait=False))
        return Response(f"A Windows update scan will performed on {agent.hostname}")


class InstallWindowsUpdates(APIView):
    permission_classes = [IsAuthenticated, AgentWinUpdatePerms]

    # install approved windows updates on agent
    def post(self, request, agent_id):
        agent = get_object_or_404(Agent, agent_id=agent_id)
        agent.delete_superseded_updates()
        agent.approve_updates()
        nats_data = {
            "func": "installwinupdates",
            "guids": agent.get_approved_update_guids(),
        }
        asyncio.run(agent.nats_cmd(nats_data, wait=False))
        return Response(f"Approved patches will now be installed on {agent.hostname}")


class EditWindowsUpdates(APIView):
    permission_classes = [IsAuthenticated, AgentWinUpdatePerms]

    # change approval status of update
    def put(self, request, pk):
        update = get_object_or_404(WinUpdate, pk=pk)

        if not _has_perm_on_agent(request.user, update.agent.agent_id):
            raise PermissionDenied()

        serializer = WinUpdateSerializer(
            instance=update, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(f"Windows update {update.kb} was changed to {update.action}")
