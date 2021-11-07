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

from django.contrib import messages
from django.core.exceptions import PermissionDenied, BadRequest
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.views.generic import FormView, DetailView, CreateView
from django.views.generic.edit import FormMixin

from gcampus.auth import exceptions, utils
from gcampus.auth.forms.token import RegisterForm
from gcampus.auth.models.token import CourseToken, AccessKey, COURSE_TOKEN_TYPE
from gcampus.core.views.base import TitleMixin


class RegisterFormView(TitleMixin, CreateView):
    form_class = RegisterForm
    title = gettext_lazy("Request Access Keys")
    template_name = "gcampusauth/forms/register.html"
    success_url = reverse_lazy("gcampuscore:course_overview")

    def form_valid(self, form):
        self.object = form.save()
        number_of_tokens: int = form.instance.number_of_tokens
        for i in range(number_of_tokens):
            access_key = AccessKey.generate_access_key()
            AccessKey(token=access_key, parent_token=self.object).save()
        messages.success(
            self.request,
            _(
                "You successfully registered a course. "
                "This page serves as an overview and allows you to view your "
                "course's access keys"
            )
        )
        # Login with course token
        utils.set_token(
            self.request, self.object.token, COURSE_TOKEN_TYPE, self.object.token_name
        )
        # return super(FormMixin, self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class RegisterSuccessView(DetailView):
    model = CourseToken
    template_name = "gcampusauth/sites/register_success.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        url_token = self.request.path.split("/")[-1]
        if url_token != kwargs["object"].token:
            raise PermissionDenied(exceptions.TOKEN_INVALID_ERROR)
        context = super().get_context_data(**kwargs)
        course_token = self.object
        context["children_token"] = AccessKey.objects.filter(parent_token=course_token)
        return context
