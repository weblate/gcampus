from django.forms import ModelForm, modelformset_factory, inlineformset_factory
from django.forms.widgets import Select, TextInput, Textarea
from leaflet.forms.widgets import LeafletWidget
from django.utils.translation import gettext_lazy as _

from gcampus.core.fields import SplitSplitDateTimeField
from gcampus.core.models import Measurement, DataPoint


class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement
        fields = ["name", "time", "location", "comment"]
        field_classes = {"time": SplitSplitDateTimeField}
        widgets = {
            "location": LeafletWidget(),
        }


class DataPointForm(ModelForm):
    """Data Point Form

    Data points (see :class:`gcampus.core.models.DataPoint`) are used
    to add data to a measurement. A data point form is always served
    in the context of a measurement, thus, the measurement itself is
    not exposed in the form.

    In most cases, it is advised to use a form set
    (see :attr:`.DataPointFormSet`).
    """

    class Meta:
        model = DataPoint
        fields = ["data_type", "value", "comment"]
        widgets = {
            "data_type": Select(attrs={"class": "form-select form-select-sm"}),
            "value": TextInput(attrs={
                "class": "form-control form-control-sm",
                "placeholder": _("Value")
            }),
            "comment": Textarea(attrs={
                "class": "form-control form-control-sm",
                "placeholder": _("Comment"),
                "rows": 2
            })
        }


DataPointFormSet = inlineformset_factory(
    Measurement, DataPoint, form=DataPointForm, can_delete=True
)
