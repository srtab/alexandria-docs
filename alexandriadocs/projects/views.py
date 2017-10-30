# -*- coding: utf-8 -*-
from accounts.mixins import HasAccessLevelMixin
from accounts.models import AccessLevel
from core.mixins import SuccessDeleteMessageMixin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from groups.models import Group
from projects.forms import (
    ImportedArchiveForm, ProjectCollaboratorForm, ProjectEditForm,
    ProjectForm, ProjectVisibilityForm)
from projects.models import Project


BADGE_URL = (
    'https://img.shields.io/badge/docs-{status}-{color}.svg?style={style}'
)


@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    """ """
    model = Project

    def get_queryset(self):
        return self.model._default_manager.collaborate(self.request.user)\
            .select_related('group')


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(SuccessMessageMixin, CreateView):
    """ """
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('projects:project-list')
    success_message = _("%(title)s was created successfully")

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        group_slug = self.request.GET.get('group')
        group = Group.objects.filter(slug=group_slug).values('pk').first()
        if not group:
            return {}
        return {'group': group.get('pk')}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProjectDetailView(DetailView):
    """ """
    model = Project

    def get_queryset(self):
        return self.model._default_manager\
            .public_or_collaborate(self.request.user)\
            .select_related('group')


class ProjectBadgeView(DetailView):
    """ """
    model = Project
    template_name_suffix = '_badge'

    def get_queryset(self):
        return self.model._default_manager\
            .public_or_collaborate(self.request.user)\
            .select_related('group')


@method_decorator(login_required, name='dispatch')
class ProjectUploadsView(HasAccessLevelMixin, DetailView):
    """ """
    model = Project
    template_name_suffix = '_uploads'
    allowed_access_level = AccessLevel.ADMIN

    def get_queryset(self):
        return self.model._default_manager.collaborate(self.request.user)\
            .select_related('group')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': ImportedArchiveForm(),
            'allowed_mimetypes': settings.PROJECTS_ALLOWED_MIMETYPES,
        })
        return context


@method_decorator(login_required, name='dispatch')
class ProjectCollaboratorsView(HasAccessLevelMixin, DetailView):
    """ """
    model = Project
    template_name_suffix = '_collaborators'
    allowed_access_level = AccessLevel.ADMIN

    def get_queryset(self):
        return self.model._default_manager.collaborate(self.request.user)\
            .select_related('group')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': ProjectCollaboratorForm()})
        return context


@method_decorator(login_required, name='dispatch')
class ProjectSettingsView(HasAccessLevelMixin, SuccessMessageMixin,
                          UpdateView):
    """ """
    model = Project
    form_class = ProjectEditForm
    template_name_suffix = '_settings'
    success_message = _("%(title)s was updated successfully")
    allowed_access_level = AccessLevel.ADMIN

    def get_queryset(self):
        return self.model._default_manager.collaborate(self.request.user)\
            .select_related('group')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'visibility_form': ProjectVisibilityForm(instance=self.object),
        })
        return context

    def get_success_url(self):
        return reverse('projects:project-settings', args=[self.object.slug])


@method_decorator(login_required, name='dispatch')
class ProjectDeleteView(HasAccessLevelMixin, SuccessDeleteMessageMixin,
                        DeleteView):
    """ """
    model = Project
    success_url = reverse_lazy('projects:project-list')
    success_message = _("%(title)s was deleted successfully")
    allowed_access_level = AccessLevel.OWNER

    def get_queryset(self):
        return self.model._default_manager.collaborate(self.request.user)


class ProjectBadgeUrlView(View):
    """ """

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        style = self.request.GET.get('style', 'flat-square')
        project = Project.objects.filter(slug=slug).first()
        if not project:
            url = BADGE_URL.format(
                status="unknown", color='lightgrey', style=style)
            return redirect(url)
        url = BADGE_URL.format(
            status="latest", color='brightgreen', style=style)
        return redirect(url)
