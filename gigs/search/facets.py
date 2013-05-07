import copy
import datetime

from django.utils.http import urlencode
class Facet(object):

    grouping = 'selected_facets'

    def __init__(self, facet_string):
        # TODO (shauno): check for presence of ":"
        field, value = facet_string.split(":", 1)
        if value:
            self.field = field
            self.value = value

    def narrow(self, queryset):
        #TODO (shauno): copy queryset
        queryset = queryset.narrow(u'%s:"%s"' % (facet.field, queryset.query.clean(facet.value)))
        return queryset

    def render_url(self):
        facet_string = '%s:%s' % (self.field, self.value)
        facet_dict = {self.get_grouping(): facet_string}
        return urlencode(facet_dict)

    def get_display(self):
        return self.value

    def get_value(self):
        return '%s:%s' % (self.field, self.value)

    def get_grouping(self):
        return self.grouping

    def narrow(self, queryset):
        #TODO (shauno): copy queryset
        queryset = queryset.narrow(u'%s:"%s"' % (self.field, queryset.query.clean(self.value)))
        return queryset

class DateFacet(Facet):

    grouping = 'selected_date_facets'

    @staticmethod
    def args_to_string(field, start, end, gap):
        return u'%s:[%s TO %s%s]' % (field, start, start, gap)

    def __init__(self, facet_string):
        #if ":" not in facet_string:
        #    continue
        field, value = facet_string.split(":", 1)
        start, to, end_gap = value.strip('[]').split()
        self.field = field
        self.start = start
        self.to = to
        end, gap = end_gap.split('+')
        self.gap = "+" + gap
        self.end = end

    def render_url(self):
        facet_string = u'%s:[%s TO %s%s]' % (self.field, self.start, self.start, self.gap)
        facet_dict = {self.get_grouping(): facet_string}
        return urlencode(facet_dict)

    def narrow(self, queryset):
        substring =" %s TO %s%s" % (self.start, self.start, self.gap)
        return queryset.narrow(u'%s:[%s]' % (self.field, substring))

    def get_value(self):
        return u'%s:[%s TO %s%s]' % (self.field, self.start, self.start, self.gap)

    def get_display(self):
        year = datetime.datetime.strptime(self.start, '%Y-%m-%dT%H:%M:%SZ').year
        return year


class FacetSet(object):

    def __init__(self, facet_string_list=[], date_facet_string_list=[]):
        self.facets = []
        self.add_facets(facet_string_list)
        self.add_date_facets(date_facet_string_list)

    def add_facet(self, facet_string):
        f = Facet(facet_string)
        if f:
            self.facets.append(f)

    def add_date_facet(self, facet_string):
        f = DateFacet(facet_string)
        if f:
            self.facets.append(f)

    def add_date_facet_args(self, field, start, end, gap):
        self.add_date_facet(DateFacet.args_to_string(field, start, end, gap))

    def add_facets(self, facet_string_list):
        for facet_string in facet_string_list:
            self.add_facet(facet_string)

    def add_date_facets(self, facet_string_list):
        for facet_string in facet_string_list:
            self.add_date_facet(facet_string)

    def has_facets(self):
        return facets != []

    def narrow(self, queryset):
        for facet in self.facets:
            queryset = facet.narrow(queryset)
        return queryset

    def get_subsets(self):
        for ind in range(len(self.facets)):
            clone = self.clone()
            f = clone.facets.pop(ind)
            yield f, clone

    def render_url(self):
        facet_list = []
        for facet in self.facets:
            facet_list.append(facet.render_url())
        return '&'.join(facet_list)

    def clone(self):
        return copy.deepcopy(self)
