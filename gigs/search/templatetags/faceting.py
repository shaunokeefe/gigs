import datetime
import copy

from django import template as django_template
from django.template.loader import render_to_string

from gigs.search.facets import FacetSet


class FacetListNode(django_template.Node):

    def __init__(self, request_path, selected_facets, query, template='search/facet_list.html'):
        self.request_path = django_template.Variable(request_path)
        self.query = django_template.Variable(query)
        self.selected_facets = django_template.Variable(selected_facets)
        self.template = template

    def render(self, context):
        try:
            request_path = self.request_path.resolve(context)
            query = self.query.resolve(context)
            selected_facets = self.selected_facets.resolve(context)
        except django_template.VariableDoesNotExist:
            return ''

        facet_list = []
        facet_list = [{'value': f.get_display(), 'other_facets': o}for f, o in selected_facets.get_subsets()]

        variables = {
                'request_path': request_path,
                'facet_list': facet_list,
                'selected_facets': selected_facets,
                'query': query
            }
        rendered_facet_list = render_to_string(self.template, variables)
        return rendered_facet_list

class FacetGroupNode(django_template.Node):

    def __init__(self, facets, facet_name, display_length, request_path, selected_facets, query, template='search/facet_group.html'):
        self.facets = django_template.Variable(facets)
        self.query = django_template.Variable(query)
        self.facet_name = facet_name
        self.display_length = display_length
        self.request_path = django_template.Variable(request_path)
        self.selected_facets = django_template.Variable(selected_facets)
        self.template = template


    def render(self, context):
        try:
            facets = self.facets.resolve(context)
            query = self.query.resolve(context)
            facet_name = self.facet_name
            display_length = self.display_length
            request_path = self.request_path.resolve(context)
            selected_facets = self.selected_facets.resolve(context)
        except django_template.VariableDoesNotExist:
            return ''
        new_facets  = []
        for facet in facets:
            facets_to_select = selected_facets.clone()
            facets_to_select.add_facet("%s:%s" % (facet_name, facet[0]))
            new_facets.append({'name': facet_name, 'count': facet[1], 'value': facet[0], 'to_select': facets_to_select})

        variables = {
                'facets':facets,
                'facets_new': new_facets,
                'query':query,
                'facet_name': facet_name,
                'display_length': display_length,
                'request_path': request_path,
                'selected_facets': selected_facets,
            }
        rendered_facet_group = render_to_string(self.template, variables)
        return rendered_facet_group

class DateFacetGroupNode(FacetGroupNode):

    def __init__(self, facets, facet_name, display_length, request_path, selected_facets, query, template='search/date_facet_group.html'):
        # TODO(shauno): fix below quick hack used to get the correct field name to facet on
        self.field = facets.split('.')[-1]
        super(DateFacetGroupNode, self).__init__(facets, facet_name, display_length, request_path, selected_facets, query, template=template)

    def render(self, context):
        try:
            facet_dict = self.facets.resolve(context)
            query = self.query.resolve(context)
            facet_list = []
            gap = facet_dict.get('gap', None)
            for date, count in facet_dict.items():
                if not date in ['end', 'gap', 'start']:
                    facet_list.append((datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').year, count, gap, date))
            facet_list.sort(key=lambda x: x[1], reverse=True)
            request_path = self.request_path.resolve(context)
            selected_facets = self.selected_facets.resolve(context)
        except django_template.VariableDoesNotExist:
            return ''

        facet_name = self.facet_name
        display_length = self.display_length
        new_facets = []
        for facet in facet_list:
            facets_to_select = selected_facets.clone()
            facets_to_select.add_date_facet_args(self.field, facet[3], facet[3], facet[2])
            new_facets.append({'name': facet_name, 'count': facet[1], 'value': facet[0], 'to_select': facets_to_select})

        variables = {
                'facets': facet_list,
                'new_facets':new_facets,
                'query':query,
                'facet_name': facet_name,
                'display_length': display_length,
                'request_path': request_path,
                'selected_facets': selected_facets,
            }
        rendered_facet_group = render_to_string(self.template, variables)
        return rendered_facet_group

# TODO (shauno): change these to inclusion tags so we can use context without all these args
def do_date_facet_group(parser, token):

    try:
        tag_name, facets, facet_name, number, request_path, selected_facets, query = token.split_contents()
    except ValueError:
        raise django_template.TemplateSyntaxError('%r tag requires 4 arguments' %
                token.contents.split()[0])
    return DateFacetGroupNode(facets, facet_name, number, request_path, selected_facets, query)

def do_facet_group(parser, token):

    try:
        tag_name, facets, facet_name, number, request_path, selected_facets, query = token.split_contents()
    except ValueError:
        raise django_template.TemplateSyntaxError('%r tag requires 4 arguments' %
                token.contents.split()[0])
    return FacetGroupNode(facets, facet_name, number, request_path, selected_facets, query)


def do_facet_list(parser, token):

    try:
        tag_name, request_path, selected_facets, query = token.split_contents()
    except ValueError:
        raise django_template.TemplateSyntaxError('%r tag requires 3 arguments' %
                token.contents.split()[0])
    return FacetListNode(request_path, selected_facets, query)

register = django_template.Library()
register.tag('facet_group', do_facet_group)
register.tag('date_facet_group', do_date_facet_group)
register.tag('current_facet_list', do_facet_list)
