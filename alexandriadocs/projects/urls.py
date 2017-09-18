# -*- coding: utf-8 -*-
from django.conf.urls import url
from projects.ajax import ImportedArchiveCreateView
from projects.views import (
    ProjectBadgeUrlView, ProjectBadgeView, ProjectCollaboratorsView,
    ProjectCreateView, ProjectDeleteView, ProjectDetailView,
    ProjectListView, ProjectSettingsView, ProjectUploadsView)


base_urlpatterns = [
    url(
        regex=r'^$',
        view=ProjectListView.as_view(),
        name='project-list'
    ),
    url(
        regex=r'^new/$',
        view=ProjectCreateView.as_view(),
        name='project-create'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        view=ProjectDetailView.as_view(),
        name='project-detail'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/badge/$',
        view=ProjectBadgeView.as_view(),
        name='project-badge'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/collaborators/$',
        view=ProjectCollaboratorsView.as_view(),
        name='project-collaborators'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/settings/$',
        view=ProjectSettingsView.as_view(),
        name='project-settings'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/delete/$',
        view=ProjectDeleteView.as_view(),
        name='project-delete'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/badge-url/$',
        view=ProjectBadgeUrlView.as_view(),
        name='project-badge-url'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/uploads/$',
        view=ProjectUploadsView.as_view(),
        name='project-uploads'
    ),
]

ajax_urlpatterns = [
    url(
        regex=r'^(?P<project_slug>[-\w]+)/uploads/new/$',
        view=ImportedArchiveCreateView.as_view(),
        name='imported-archive-create'
    ),
]

urlpatterns = base_urlpatterns + ajax_urlpatterns
