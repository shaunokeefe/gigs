from django import template

register = template.Library()


@register.inclusion_tag('search/search_results.html', takes_context=True)
def search_results(context):
    request = context['request']
    #keys = ('selected_date_facets', 'selected_facets')
    #get_args = {}
    #for key in keys:
    #    val = request.session.get(key)
    #    if val:
    #        get_args[key] = val
    query = request.session.get('search_results_query', None)
    selected_facets = request.session.get('selected_facets', None)

    # TODO add query to search url resolved by name
    return {
        'search_results_query': query,
        'selected_facets': selected_facets
        #'get_args': get_args,
        #'search_url': request.session.get('search_url', None)
    }
