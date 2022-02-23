import operator

from django.db.models import Q
from functools import reduce
from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from .models import Agent, Groups

class GroupSerializer(serializers.ModelSerializer):
    agents = serializers.SerializerMethodField()
    
    def get_agents(self, obj):
        # This needs to be looked at, once this is fixed we can count the agents and do other stuff with it
        agents = Agent.objects.filter(groups__contains=[obj.id]).count()
        return agents

    class Meta:
        model = Groups
        fields = "__all__"