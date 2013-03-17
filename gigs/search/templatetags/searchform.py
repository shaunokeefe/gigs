#import datetime
#import copy
#
from django import template as django_template
from django.template.loader import render_to_string

register = django_template.Library()

class SearchFormNode(django_template.Node):

    def __init__(self, size):
        self.size = size
        suffix = ''
        if self.size:
            suffix = '_' + size
        self.template = 'search/search_form%s.html' % (suffix)

    def render(self, context):
        query = None
        try:
            query = django_template.Variable('query').resolve(context)

        except django_template.VariableDoesNotExist:
            pass

        variables = {
                'query': query,
            }
        rendered_search_form = render_to_string(self.template, variables)
        return rendered_search_form

def do_search_form(parser, token):
    try:
        tag_name, size = token.split_contents()
        size = size.strip('"')
    except ValueError:
        raise django_template.TemplateSyntaxError('%r tag requires 1 argument' %
                token.contents.split()[0])
    return SearchFormNode(size)

register.tag('search_form', do_search_form)
