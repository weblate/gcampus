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

__all__ = [
    "CourseOverviewFormView",
    "deactivate_access_key",
    "activate_access_key",
    "generate_new_access_keys",
]

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic.edit import UpdateView

from gcampus.auth import session, exceptions
from gcampus.auth.decorators import require_course_token
from gcampus.auth.fields.token import check_form_and_request_token
from gcampus.auth.models.token import AccessKey, CourseToken, course_updated
from gcampus.auth.session import get_token
from gcampus.auth.forms.course_overview import (
    CourseOverviewForm,
    GenerateAccessKeysForm,
)
from gcampus.core.views.base import TitleMixin

TOKEN_FIELD_NAME = "gcampus_auth_token"


class CourseOverviewFormView(TitleMixin, UpdateView):
    form_class = CourseOverviewForm
    model = CourseToken
    title = _("Course Administration")
    template_name = "gcampusauth/sites/course_overview.html"

    def __init__(self, *args, **kwargs):
        super(CourseOverviewFormView, self).__init__(*args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        token = session.get_token(self.request)
        return get_object_or_404(queryset, token=token)

    @method_decorator(require_course_token)
    def dispatch(self, request, *args, **kwargs):
        return super(CourseOverviewFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form: CourseOverviewForm):
        check_form_and_request_token(form, self.request)
        form.save()
        # Update token name
        session.set_token(
            self.request, form.instance.token, "course", form.instance.token_name
        )
        return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        if "access_keys" not in kwargs:
            kwargs["access_keys"] = AccessKey.objects.filter(parent_token=self.object)
        if "generate_accesskeys_form" not in kwargs:
            kwargs["generate_accesskeys_form"] = GenerateAccessKeysForm()
        if "register_max_access_key" not in kwargs:
            kwargs["register_max_access_key"] = settings.REGISTER_MAX_ACCESS_KEY_NUMBER
        return super().get_context_data(**kwargs)


@require_POST
@require_course_token
def deactivate_access_key(request, pk):
    access_key = get_object_or_404(AccessKey, pk=pk, deactivated=False)
    parent_token = get_token(request)
    if access_key.parent_token.token == parent_token:
        access_key.deactivated = True
        access_key.save()
        return redirect("gcampusauth:course-overview")
    else:
        raise PermissionDenied(exceptions.TOKEN_INVALID_ERROR)


@require_POST
@require_course_token
def activate_access_key(request, pk):
    access_key = get_object_or_404(AccessKey, pk=pk, deactivated=True)
    parent_token = get_token(request)
    if access_key.parent_token.token == parent_token:
        access_key.deactivated = False
        access_key.save()
        return redirect("gcampusauth:course-overview")
    else:
        raise PermissionDenied(exceptions.TOKEN_INVALID_ERROR)


@require_POST
@require_course_token
def generate_new_access_keys(request):
    form = GenerateAccessKeysForm(request.POST)
    token = get_token(request)
    course_token = CourseToken.objects.get(token=token)
    if form.is_valid():
        count = form.cleaned_data["count"]
        max_count = getattr(settings, "REGISTER_MAX_ACCESS_KEY_NUMBER", 30)
        current_count = AccessKey.objects.filter(parent_token=course_token).count()

        allowed_count = max_count - current_count
        if count > allowed_count:
            messages.error(
                request,
                gettext(
                    "You are only allowed to generate a total of {max_count:d} access "
                    "keys. You have currently registered {current_count:d} access keys "
                    "and can only generate {allowed_count:d} more."
                ).format(
                    max_count=max_count,
                    current_count=current_count,
                    allowed_count=allowed_count,
                ),
            )
            return redirect("gcampusauth:course-overview")

        with transaction.atomic():
            for i in range(count):
                access_key = AccessKey.generate_access_key()
                AccessKey(token=access_key, parent_token=course_token).save()
        course_updated.send(sender=GenerateAccessKeysForm, instance=course_token)

        messages.success(
            request,
            gettext("You successfully generated {count:d} new access keys").format(
                count=count
            ),
        )
    else:
        for errors in form.errors.values():
            for error in errors:
                messages.error(request, error)
    return redirect("gcampusauth:course-overview")
