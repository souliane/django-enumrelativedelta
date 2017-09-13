from enum import Enum
from enumfields.fields import EnumFieldMixin
from relativedeltafield import RelativeDeltaField, format_relativedelta
from dateutil import relativedelta


class EnumRelativeDeltaField(EnumFieldMixin, RelativeDeltaField):
    """Define an EnumField that takes relativedelta as values."""

    def deconstruct(self):
        name, path, args, kwargs = super(EnumRelativeDeltaField, self).deconstruct()
        if 'default' in kwargs:
            if isinstance(kwargs["default"], relativedelta.relativedelta):
                kwargs["default"] = format_relativedelta(kwargs["default"])

        return name, path, args, kwargs

    def get_db_prep_value(self, value, connection, prepared=False):  # noqa
        if value is None:
            return value
        else:
            return format_relativedelta(
                RelativeDeltaField.to_python(
                    self, value.value if isinstance(value, Enum) else value
                )
            )
