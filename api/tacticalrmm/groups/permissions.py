from django.shortcuts import get_object_or_404
from rest_framework import permissions

from tacticalrmm.permissions import _has_perm, _has_perm_on_group

class GroupsPerms(permissions.BasePermission):
    def has_permission(self, r, view):
        if r.method == "GET" or r.method == "PATCH":
            if "pk" in view.kwargs.keys():
                return _has_perm(r, "can_list_groups") and _has_perm_on_group(
                    r.user, view.kwargs["pk"]
                )
            else:
                return _has_perm(r, "can_list_groups")
        else:
            if "pk" in view.kwargs.keys():
                return _has_perm(r, "can_manage_groups") and _has_perm_on_group(
                    r.user, view.kwargs["pk"]
                )
            else:
                return _has_perm(r, "can_manage_groups")