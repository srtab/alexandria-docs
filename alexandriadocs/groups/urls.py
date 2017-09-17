# -*- coding: utf-8 -*-
from django.conf.urls import url

from groups.views import (
    GroupCollaboratorsView, GroupCreateView, GroupDeleteView, GroupDetailView,
    GroupListView, GroupSettingsView)


urlpatterns = [
    url(
        regex=r'^$',
        view=GroupListView.as_view(),
        name='group-list'
    ),
    url(
        regex=r'^new/$',
        view=GroupCreateView.as_view(),
        name='group-create'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        view=GroupDetailView.as_view(),
        name='group-detail'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/collaborators/$',
        view=GroupCollaboratorsView.as_view(),
        name='group-collaborators'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/settings/$',
        view=GroupSettingsView.as_view(),
        name='group-settings'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/settings/delete/$',
        view=GroupDeleteView.as_view(),
        name='group-delete'
    )
]
