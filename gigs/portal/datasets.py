from django_tablib import datasets
from django_tablib.models import DatasetMetaclass
from django.db.models.fields.related import ForeignKey

class RelatedDataset(datasets.SimpleDataset):

    def _getattrs(self, obj):
        attrs = []
        for attr_string in self.attr_list:
            current_obj = obj
            attr_parts = attr_string.split('.')
            while attr_parts:
                attr_part = attr_parts.pop(0)
                if len(attr_parts):
                    current_obj = getattr(current_obj, attr_part)
                    continue

                if callable(attr_part):
                    value = self._cleanval(attr_part(current_obj), attr_part)
                else:
                    value = self._cleanval(getattr(current_obj, attr_part), attr_part)
                attrs.append(value)
                break
        return attrs

class ModelRelatedDataset(RelatedDataset):

    fields  = None
    headers = None

    def __init__(self, queryset, **kwargs):
        self.model = queryset.model
        if self.fields is not None:
            fields = self.fields
        else:
            fields = self._get_fields(self.model)
        
        kwargs['headers'] = fields
        super(ModelRelatedDataset, self).__init__(queryset, **kwargs)

    def _get_fields(self, model):
        fields = model._meta.fields
        field_names = []

        for field in [f for f in fields if not isinstance(f, ForeignKey)]:
            if field.name != 'id':
                field_names.append(field.name)

        for field in [f for f in fields if isinstance(f, ForeignKey)]:
            related_model_class = field.rel.to
            related_fields = self._get_fields(related_model_class)
            related_fields = [related_model_class.__name__.lower() + '.' + rf for rf in related_fields]
            field_names.extend(related_fields)

        return field_names
