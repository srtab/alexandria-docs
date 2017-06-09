# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView

from projects.models import Project


class HomepageView(ListView):
    """ """
    template_name = "homepage.html"
    model = Project
    paginate_by = 3 * 5  # elems per line * num lines