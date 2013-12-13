from django.db.models import ForeignKey

from import_export.fields import Field
from import_export.resources import modelresource_factory


class RelatedResourceField(Field):
    """Export fields from related Models

    Use a resource defined for a related model
    to export the fields for that model
    """

    def __init__(self, related_resource, *args, **kwargs):
        self.related_resource = related_resource
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

        rendered_values = []
        related_resource_instance = modelresource_factory(model, self.related_resource)
        return related_resource_instance().export_resource(value)

class RelatedM2MResourceField(RelatedResourceField):
    """Export fields from related Models

    Use a resource defined for a related model
    to export the fields for that model
    """

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
        related_resource_instance = modelresource_factory(model, self.related_resource)
        for value in values:
            rendered_values.extend(related_resource_instance().export_resource(value))
        return rendered_values
