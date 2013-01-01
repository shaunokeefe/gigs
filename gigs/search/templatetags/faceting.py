import datetime
import copy

from django import template as django_template
from django.template.loader import render_to_string


class FacetListNode(django_template.Node):

    def __init__(self, request_path, selected_facets, selected_date_facets, template='search/facet_list.html'):
        self.request_path = django_template.Variable(request_path)
        self.selected_facets = django_template.Variable(selected_facets)
        self.selected_date_facets = django_template.Variable(selected_date_facets)
        self.template = template

    def render(self, context):
        try:
            request_path = self.request_path.resolve(context)
            selected_facets = self.selected_facets.resolve(context)
            selected_date_facets = self.selected_date_facets.resolve(context)
        except django_template.VariableDoesNotExist:
            return ''

        facet_list = []
        for facet in selected_facets:
            value = facet.split(':')[1]
            sf_copy = copy.copy(selected_facets)
            sf_copy.remove(facet)
            facet_list.append({'value':value, 'other_facets':sf_copy})

        date_facet_list = []
        for facet in selected_date_facets:
            sdf_copy = copy.copy(selected_date_facets)
            sdf_copy.remove(facet)
            # TODO (shauno): date stuff needs to handle months and days etc
            year = facet.split(':')[1]
            year = year.strip('[]')
            year = year.split('-')[0]
            date_facet_list.append({'value':year, 'other_facets':sdf_copy})

        variables = {
                'request_path': request_path,
                'facet_list': facet_list,
                'date_facet_list': date_facet_list,
                'selected_facets': selected_facets,
                'selected_date_facets': selected_date_facets
            }
        rendered_facet_list = render_to_string(self.template, variables)
        return rendered_facet_list

class FacetGroupNode(django_template.Node):

    def __init__(self, facets, facet_name, display_length, request_path, selected_facets, selected_date_facets, template='search/facet_group.html'):
        self.facets = django_template.Variable(facets)
        self.facet_name = facet_name
        self.display_length = display_length
        self.request_path = django_template.Variable(request_path)
        self.selected_facets = django_template.Variable(selected_facets)
        self.selected_date_facets = django_template.Variable(selected_date_facets)
        self.template = template


    def render(self, context):
        try:
            facets = self.facets.resolve(context)
            facet_name = self.facet_name
            display_length = self.display_length
            request_path = self.request_path.resolve(context)
            selected_facets = self.selected_facets.resolve(context)
            selected_date_facets = self.selected_date_facets.resolve(context)
        except django_template.VariableDoesNotExist:
            return ''
        variables = {
                'facets':facets,
                'facet_name': facet_name,
                'display_length': display_length,
                'request_path': request_path,
                'selected_facets': selected_facets,
                'selected_date_facets': selected_date_facets
            }
        rendered_facet_group = render_to_string(self.template, variables)
        return rendered_facet_group

class DateFacetGroupNode(FacetGroupNode):

    def __init__(self, facets, facet_name, display_length, request_path, selected_facets, selected_date_facets, template='search/date_facet_group.html'):
        super(DateFacetGroupNode, self).__init__(facets, facet_name, display_length, request_path, selected_facets, selected_date_facets, template=template)

    def render(self, context):
        try:
            facet_dict = self.facets.resolve(context)
            facet_list = []
            gap = facet_dict.get('gap', None)
            for date, count in facet_dict.items():
                if not date in ['end', 'gap', 'start']:
                    facet_list.append((datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').year, count, gap, date))
            facet_list.sort(key=lambda x: x[1], reverse=True)
            request_path = self.request_path.resolve(context)
            selected_facets = self.selected_facets.resolve(context)
            selected_date_facets = self.selected_date_facets.resolve(context)
        except django_template.VariableDoesNotExist:
            return ''
        facet_name = self.facet_name
        display_length = self.display_length
        variables = {
                'facets':facet_list,
                'facet_name': facet_name,
                'display_length': display_length,
                'request_path': request_path,
                'selected_facets': selected_facets,
                'selected_date_facets': selected_date_facets
            }
        rendered_facet_group = render_to_string(self.template, variables)
        return rendered_facet_group


def do_date_facet_group(parser, token):

    try:
        tag_name, facets, facet_name, number, request_path, selected_facets, selected_date_facets = token.split_contents()
    except ValueError:
        raise django_template.TemplateSyntaxError('%r tag requires 4 arguments' %
                token.contents.split()[0])
    return DateFacetGroupNode(facets, facet_name, number, request_path, selected_facets, selected_date_facets)

def do_facet_group(parser, token):

    try:
        tag_name, facets, facet_name, number, request_path, selected_facets, selected_date_facets = token.split_contents()
    except ValueError:
        raise django_template.TemplateSyntaxError('%r tag requires 4 arguments' %
                token.contents.split()[0])
    return FacetGroupNode(facets, facet_name, number, request_path, selected_facets, selected_date_facets)

def do_facet_list(parser, token):

    try:
        tag_name, request_path, selected_facets, selected_date_facets = token.split_contents()
    except ValueError:
        raise django_template.TemplateSyntaxError('%r tag requires 3 arguments' %
                token.contents.split()[0])
    return FacetListNode(request_path, selected_facets, selected_date_facets)

register = django_template.Library()
register.tag('facet_group', do_facet_group)
register.tag('date_facet_group', do_date_facet_group)
register.tag('current_facet_list', do_facet_list)
