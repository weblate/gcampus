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
import string
from typing import Optional, List

from django import template
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.template import Context
from django.template import Node
from django.template.base import FilterExpression
from django.template.base import token_kwargs
from django.utils.html import format_html
from django_filters.constants import EMPTY_VALUES

from gcampus.auth import session
from gcampus.auth.exceptions import TOKEN_EMPTY_ERROR
from gcampus.auth.models.token import (
    can_token_edit_measurement,
    TokenType, get_token_type_from_token,
)
from gcampus.core.models import Measurement

register = template.Library()
_html_token_separator = '<span class="token-separator"></span>'


class AuthTokenNode(Node):
    def __init__(self, prefix: Optional[FilterExpression] = None):
        self.prefix_token = prefix
        super(AuthTokenNode, self).__init__()

    def render(self, context):
        if "request" not in context:
            raise ValueError("Unable to find 'request' in template context!")
        token = session.get_token(context.request)
        if token in EMPTY_VALUES or token == "None":
            raise PermissionDenied(TOKEN_EMPTY_ERROR)
        if self.prefix_token is not None:
            prefix = f"{self.prefix_token.resolve(context)}-"
        else:
            prefix = ""
        if token:
            return format_html(
                '<input type="hidden" name="{}gcampus_auth_token" value="{}">',
                prefix,
                token,
            )
        else:
            return ""


@register.simple_tag(takes_context=True)
def save_token(context: Context) -> str:
    request: HttpRequest = context["request"]
    return session.get_token(request)


@register.simple_tag(takes_context=True)
def save_token_type(context: Context) -> str:
    request: HttpRequest = context["request"]
    return session.get_token_type(request).value


@register.tag
def auth_token(parser, token):  # noqa
    tokens = token.split_contents()
    if len(tokens) == 2:
        kwargs = token_kwargs(tokens[1:], parser)
        return AuthTokenNode(**kwargs)
    elif len(tokens) == 1:
        return AuthTokenNode()
    else:
        raise ValueError("'auth_token' takes only one keyword argument 'prefix'")


@register.filter
def can_edit(measurement: Measurement, request: HttpRequest) -> bool:
    """Can Edit Authentication Filter

    Django template filter used to check whether a measurement can be
    edited by the user of the current request.

    Usage:

    .. code::

        {% load auth_token %}
        ...
        {% if measurement|can_edit:request %}
            ...
        {% endif %}

    :param measurement: The measurement used to check the permission.
    :param request: Additional parameter passed to the filter to provide
        the current session which may contain the token of the user.
    :returns: Boolean whether or not the current user is allowed to edit
        the provided measurement.
    """
    token = session.get_token(request)
    if token is None:
        return False
    token_type: TokenType = session.get_token_type(request)
    return can_token_edit_measurement(token, measurement, token_type=token_type)


@register.inclusion_tag("gcampusauth/styles/token.html")
def displaytoken_head() -> dict:
    return {}


@register.inclusion_tag("gcampusauth/js/token_toggle.html")
def displaytoken_js() -> dict:
    return {}


@register.inclusion_tag("gcampusauth/components/token.html")
def displaytoken(
    token: str,
    css_class: Optional[str] = None,
    hidden: bool = True,
    toggle: bool = False,
) -> dict:
    token_length: int = len(token)
    token_type: TokenType = get_token_type_from_token(token)

    # Generate the HTML for the token
    token_html: List[str] = [_wrap_token_character(c) for c in token]
    token_hidden_html: List[str] = [
        _wrap_token_character(c, hide=(i < token_length - 3))
        for i, c in enumerate(token)
    ]

    # Add separator
    token_html = token_html[:4] + [_html_token_separator] + token_html[4:]
    token_hidden_html = (
        token_hidden_html[:4] + [_html_token_separator] + token_hidden_html[4:]
    )
    if token_type is TokenType.course_token:
        # Add second separator for the course token
        token_html = token_html[:9] + [_html_token_separator] + token_html[9:]
        token_hidden_html = (
            token_hidden_html[:9] + [_html_token_separator] + token_hidden_html[9:]
        )

    return {
        "token": token,
        "token_html": "".join(token_html),
        "token_hidden_html": "".join(token_hidden_html),
        "css_class": css_class,
        "hidden": hidden,
        "toggle": toggle,
        "has_clear": bool(toggle or not (hidden or toggle)),
    }


def _wrap_token_character(character: str, hide: bool = False) -> str:
    if not len(character) == 1:
        raise ValueError(f"Expected a single character but got {len(character)}")
    # make sure character is in upper case
    character = character.upper()
    character_type: str
    if character in string.digits:
        character_type = "digit"
    elif character in string.ascii_uppercase:
        character_type = "letter"
    else:
        raise ValueError(f"Invalid token character {character}")
    if hide:
        return f'<span class="token-char token-hidden">*</span>'
    return f'<span class="token-char token-{character_type}">{character}</span>'
