from django.db.models import ForeignKey
from django.db.models import Count, Max

from import_export.fields import Field
from import_export.resources import modelresource_factory


class RelatedResourceField(Field):
    """Export fields from related Models

    Use a resource defined for a related model
    to export the fields for that model
    """

    def __init__(self, related_resource, *args, **kwargs):
        self.model =  related_resource._meta.model
        self.related_resource =  modelresource_factory(self.model, related_resource)()
        super(RelatedResourceField, self).__init__(*args, **kwargs)

class RelatedForeignKeyResourceField(RelatedResourceField):

    def export(self, obj):
        value = self.get_value(obj)
        if value is None:
            return []
        field_object, model, direct, m2m = obj._meta.get_field_by_name(self.attribute)

        # Check if, for whatever reason, we're not a fk
        if not isinstance(field_object, ForeignKey):
            return super(RelatedResourceField, self).export(obj)

        model = value.__class__

        return self.related_resource.export_resource(value)


class RelatedM2MResourceField(RelatedResourceField):
    """Export fields from related Models

    Use a resource defined for a related model
    to export the fields for that model
    """
    def get_max_num_related(self, obj):
        count = obj.__class__.objects.all().annotate(num=Count(self.attribute)).aggregate(max=Max('num'))['max']
        return count

    def export(self, obj):
        value = self.get_value(obj)
        if value is None:
            return []

        field_object, model, direct, m2m = obj._meta.get_field_by_name(self.attribute)

        # Check if, for whatever reason, we're not a fk
        if not m2m and not isinstance(field_object, ForeignKey):
            return super(RelatedResourceField, self).export(obj)

        model =  value.model

        values = value.all()
        rendered_values = []
        for value in values:
            rendered_values.extend(self.related_resource.export_resource(value))

        # pad out
        values_per_entry = len(self.related_resource.get_export_headers())
        pad_len = (self.get_max_num_related(obj) - len(values)) * values_per_entry
        rendered_values.extend([None] * pad_len)

        return rendered_values
