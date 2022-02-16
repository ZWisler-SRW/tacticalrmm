import pytz
from rest_framework import serializers

from .models import Agent, WinUpdate, WinUpdatePolicy, WinUpdateManager


class WinUpdateSerializer(serializers.ModelSerializer):
    date_installed = serializers.SerializerMethodField()

    def get_date_installed(self, obj):
        if obj.date_installed is not None:
            return obj.date_installed.astimezone(self.context["default_tz"]).strftime(
                "%m %d %Y %H:%M"
            )
        return None

    class Meta:
        model = WinUpdate
        fields = "__all__"

class WinUpdateManagerSerializer(serializers.ModelSerializer):
    update_data = serializers.SerializerMethodField()

    def get_update_data(self, obj):
        update = WinUpdate.objects.filter(kb=obj.kb)
        obj.data = {
            "description": update.first().description,
            "categories": update.first().categories,
            "more_info_urls": update.first().more_info_urls,
            "support_url": update.first().support_url,
            "pending_agents": Agent.objects.filter(id__in=update.filter(installed=False).values_list('agent', flat=True)).values_list('hostname', flat=True),
            "installed_agents": Agent.objects.filter(id__in=update.filter(installed=True).values_list('agent', flat=True)).values_list('hostname', flat=True)
        }
        return obj.data

    class Meta:
        model = WinUpdateManager
        fields = "__all__"

class WinUpdatePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = WinUpdatePolicy
        fields = "__all__"


class ApprovedUpdateSerializer(serializers.ModelSerializer):
    winupdates = WinUpdateSerializer(read_only=True)
    agentid = serializers.ReadOnlyField(source="agent.pk")
    patch_policy = serializers.SerializerMethodField("get_policies")

    def get_policies(self, obj):
        policy = WinUpdatePolicy.objects.get(agent=obj.agent)
        return WinUpdatePolicySerializer(policy).data

    class Meta:
        model = WinUpdate
        fields = (
            "id",
            "kb",
            "guid",
            "agentid",
            "winupdates",
            "patch_policy",
        )
