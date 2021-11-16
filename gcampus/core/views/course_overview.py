#  Copyright (C) 2021 desklab gUG (haftungsbeschränkt)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from abc import ABC
from typing import Union, Optional

from django.core.exceptions import (
    PermissionDenied,
    ObjectDoesNotExist,
    SuspiciousOperation,
    FieldError, ValidationError
)
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic.edit import FormView
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext

from django.contrib import messages

from gcampus.auth import utils, exceptions
from gcampus.auth.exceptions import TOKEN_INVALID_ERROR, TOKEN_CREATE_PERMISSION_ERROR
from gcampus.auth.forms.token import AccessKeyForm, CourseTokenForm, TOKEN_FIELD_NAME
from gcampus.auth.models.token import (
    ACCESS_TOKEN_TYPE,
    COURSE_TOKEN_TYPE,
    CourseToken,
    can_token_create_measurement,
)
from gcampus.auth.utils import get_token
from gcampus.core.forms.course_overview import CourseOverviewForm, GenerateAccesskeysForm
from gcampus.core.models import Measurement
from gcampus.auth.models.token import AccessKey, CourseToken

from django.views.generic import ListView
from django import forms

from gcampus.core.views.measurement_visibility import _check_general_permission
from gcampus.settings.base import REGISTER_MAX_TOKEN_NUMBER

TOKEN_FIELD_NAME = "gcampus_auth_token"


class AssociatedAccessKeys(ListView):
    template_name = "gcampuscore/sites/overview/course_overview.html"
    model = Measurement
    context_object_name = "measurement_list"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        token = utils.get_token(self.request)
        if token is None:
            raise PermissionDenied(exceptions.TOKEN_EMPTY_ERROR)
        # TODO: We might want to check whether the provided token exists
        #   and whether or not it is disabled. If it does not exists,
        #   the page will just be empty which is also ok.
        # Check if provided token is actually a course token
        token_type = utils.get_token_type(self.request)
        if token_type != COURSE_TOKEN_TYPE:
            raise PermissionDenied(exceptions.TOKEN_INVALID_ERROR)
        access_keys = AccessKey.objects.filter(parent_token__token=token)
        measurements = Measurement.all_objects.filter(token__parent_token__token=token)
        context["access_keys"] = access_keys
        context["measurements"] = measurements
        return context


class CourseOverviewFormView(FormView):
    template_name = "gcampuscore/sites/overview/course_overview.html"
    form_class = CourseOverviewForm
    next_view_name = "gcampuscore/sites/overview/course_overview.html"

    def __init__(self, *args, **kwargs):
        super(CourseOverviewFormView, self).__init__(*args, **kwargs)
        self.instance: Optional[CourseToken] = None

    def get_form_kwargs(self) -> dict:
        kwargs: dict = super(CourseOverviewFormView, self).get_form_kwargs()
        kwargs["instance"] = self.instance
        return kwargs

    def get(self, request, *args, **kwargs):
        token = utils.get_token(request)
        token_type = utils.get_token_type(request)
        if token_type == COURSE_TOKEN_TYPE and token is not None:
            self.instance = CourseToken.objects.get(token=token)
            return super(CourseOverviewFormView, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        token = utils.get_token(request)
        token_type = utils.get_token_type(request)
        if token_type == COURSE_TOKEN_TYPE and token is not None:
            self.instance = CourseToken.objects.get(token=token)
            return super(CourseOverviewFormView, self).post(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def form_valid(self, form: CourseOverviewForm):
        form_token = form.cleaned_data[TOKEN_FIELD_NAME]
        session_token = utils.get_token(self.request)
        if form_token != session_token:
            # Someone modified the session or token provided by the form
            raise SuspiciousOperation()
        form.save()
        # Update token name
        utils.set_token(
            self.request, form.instance.token, "course", form.instance.token_name
        )
        return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        token = utils.get_token(self.request)
        access_keys = AccessKey.objects.filter(parent_token__token=token)
        context["access_keys"] = access_keys
        context["generate_accesskeys_form"] = GenerateAccesskeysForm()
        return context


@require_POST
def deactivate_accesskey(request, pk):
    access_key = AccessKey.objects.get(pk=pk)
    parent_token = get_token(request)
    if parent_token is not None and access_key:
        if access_key.parent_token.token == parent_token:
            # context = {'measurement': measurement[0]}
            access_key.deactivated = True
            access_key.save()
            return redirect("gcampuscore:course_overview")
        else:
            raise PermissionDenied(exceptions.TOKEN_INVALID_ERROR)
    else:
        if not access_key:
            raise ObjectDoesNotExist(_("The Accesskey is probably already deactivated"))
        if not parent_token:
            raise PermissionDenied(exceptions.TOKEN_EMPTY_ERROR)


@require_POST
def activate_accesskey(request, pk):
    access_key = AccessKey.objects.get(pk=pk)
    parent_token = get_token(request)
    if parent_token is not None and access_key:
        if access_key.parent_token.token == parent_token:
            # context = {'measurement': measurement[0]}
            access_key.deactivated = False
            access_key.save()
            return redirect("gcampuscore:course_overview")
        else:
            raise PermissionDenied(exceptions.TOKEN_INVALID_ERROR)
    else:
        if not access_key:
            raise ObjectDoesNotExist(_("The Accesskey is probably already deactivated"))
        if not parent_token:
            raise PermissionDenied(exceptions.TOKEN_EMPTY_ERROR)


@require_POST
def generate_new_accesskeys(request):
    if request.method == 'POST':
        form = GenerateAccesskeysForm(request.POST)
        token = get_token(request)
        coursetoken_object = CourseToken.objects.get(token=token)
        if form.is_valid():
            num_generate_accesskeys = form.cleaned_data["generate_accesskeys"]

            old_accesskeys = AccessKey.objects.filter(parent_token=coursetoken_object)
            num_old_accesskeys = len(old_accesskeys)

            if num_old_accesskeys + num_generate_accesskeys > REGISTER_MAX_TOKEN_NUMBER:
                messages.warning(
                    request,
                    gettext(
                        f"You are only allowed to generate {REGISTER_MAX_TOKEN_NUMBER} Accesskeys per Coursetoken. "
                        f"You currently have registered {num_old_accesskeys} Accesskeys. You can only "
                        f"generate {REGISTER_MAX_TOKEN_NUMBER - num_old_accesskeys} additional Accesskeys."
                    ))
                return redirect("gcampuscore:course_overview")

            coursetoken: CourseToken = get_object_or_404(CourseToken, token=token)
            for i in range(num_generate_accesskeys):
                access_key = AccessKey.generate_access_key()
                AccessKey(token=access_key, parent_token=coursetoken).save()

            messages.success(
                request,
                gettext(f'You successfully generated {num_generate_accesskeys} new Accesskeys.'))
            return redirect("gcampuscore:course_overview")

    # Return blank form if GET request
    else:
        form = GenerateAccesskeysForm()

    return render(request, "gcampuscore/sites/overview/course_overview.html", {'form': form})
