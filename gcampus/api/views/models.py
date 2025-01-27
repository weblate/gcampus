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

from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework_gis.pagination import GeoJsonPagination

from gcampus.api.serializers import (
    MeasurementSerializer,
    ParameterTypeSerializer,
    ParameterSerializer,
)
from gcampus.core.models import Measurement, ParameterType, Parameter


class MeasurementAPIViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
    queryset = Measurement.objects.order_by("time").all()
    serializer_class = MeasurementSerializer
    pagination_class = GeoJsonPagination


class ParameterTypeAPIViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
    queryset = ParameterType.objects.order_by("name").all()
    serializer_class = ParameterTypeSerializer
    pagination_class = PageNumberPagination


class ParameterAPIViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
    queryset = Parameter.objects.order_by("measurement__time").all()
    serializer_class = ParameterSerializer
    pagination_class = PageNumberPagination
