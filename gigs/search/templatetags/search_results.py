from django import template

register = template.Library()


@register.inclusion_tag('search/search_results.html', takes_context=True)
def search_results(context):
    request = context['request']
    selected_facets = request.session.get('selected_facets', None)
    # TODO add query to search url resolved by name
    return {
        'selected_facets': selected_facets
    }
