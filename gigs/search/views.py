from django.conf import settings
from haystack.views import FacetedSearchView#, basic_search
from gigs.search.models import SearchQueryRecord

from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack.forms import ModelSearchForm
from haystack.query import EmptySearchQuerySet, SearchQuerySet

class LoggedSearchView(FacetedSearchView):

    def __call__(self, request):
        response = super(LoggedSearchView, self).__call__(request)
        query = SearchQueryRecord(
                query = self.query,
                result_count = self.results.count()
                )
        if not request.user.is_anonymous():
            query.user = request.user 
        query.save()

        return response

    def build_form(self, form_kwargs=None):
        if form_kwargs is None:
            form_kwargs = {}

        # This way the form can always receive a list containing zero or more
        # facet expressions:
        form_kwargs['selected_date_facets'] = self.request.GET.getlist("selected_date_facets")

        return super(LoggedSearchView, self).build_form(form_kwargs)

    def extra_context(self):
        extra = super(LoggedSearchView, self).extra_context()
        extra['selected_facets'] = self.request.GET.getlist('selected_facets')
        extra['selected_date_facets'] = self.request.GET.getlist('selected_date_facets')
        return extra

column_name_map = {
        0: 'tmp',
        1:'start',
        2:'venue_name',
        3:'bands',
        4:'name',
        5:'cost',
        6:'venue_location',
    }

def ajax_search_view(request):
    page_length = request.GET.get('iDisplayLength', None)
    display_start = request.GET.get('iDisplayStart', None)
    num_sorting_cols = request.GET.get('iSortingCols', None)

    sorting=[]
    if num_sorting_cols:
        for column_num in range(0,int(num_sorting_cols)):
            column_id = int(request.GET.get('iSortCol_'+str(column_num),0))
            if request.GET.get('bSortable_{0}'.format(column_id), 'false')  == 'true':  # make sure the column is sortable first
                sort_column_name = column_name_map[column_id]
                sorting_direction = request.GET.get('sSortDir_'+ str(column_num), 'asc')
                if sorting_direction == 'desc':
                    sort_column_name = '-' + sort_column_name
                sorting.append(sort_column_name)

    extra_context = {
                'sEcho': request.GET.get('sEcho', None),
                #'iTotalRecords': 10000,
                'iTotalDisplayRecords':page_length,
                }

    get_copy = request.GET.copy()
    get_copy['page'] = int(display_start) / int(page_length) + 1
    request.GET = get_copy
    return basic_search(request, template='search/search.json',
           results_per_page=page_length,
           extra_context=extra_context, sort_by=sorting)

def basic_search(request, template='search/search.html', load_all=True, form_class=ModelSearchForm, searchqueryset=None, context_class=RequestContext, extra_context=None, results_per_page=None, sort_by=[]):
    """
    A more traditional view that also demonstrate an alternative
    way to use Haystack.

    Useful as an example of for basing heavily custom views off of.

    Also has the benefit of thread-safety, which the ``SearchView`` class may
    not be.

    Template:: ``search/search.html``
    Context::
        * form
          An instance of the ``form_class``. (default: ``ModelSearchForm``)
        * page
          The current page of search results.
        * paginator
          A paginator instance for the results.
        * query
          The query received by the form.
    """
    query = ''
    results = EmptySearchQuerySet()

    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)

        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=searchqueryset, load_all=load_all)
        results = SearchQuerySet().all()

    selected_facets = request.GET.getlist('selected_facets')
    for facet in selected_facets:
        if ":" not in facet:
            continue
        field, value = facet.split(":", 1)
        if value:
            results = results.narrow(u'%s:"%s"' % (field, results.query.clean(value)))

    selected_date_facets = request.GET.getlist('selected_date_facets')
    for facet in selected_date_facets:
        if ":" not in facet:
            continue
        field, value = facet.split(":", 1)

        if value:
            start, to, end, gap = value.strip('[]').split()
            results = results.narrow(u'%s:[%s TO %s+%s]' % (field, start, start, gap))

    results = results.order_by(*sort_by)
    if not template:
        return results
    count = results.count()
    paginator = Paginator(results, results_per_page or RESULTS_PER_PAGE)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
        'query': query,
        'suggestion': None,
        'count': count,
    }

    if getattr(settings, 'HAYSTACK_INCLUDE_SPELLING', False):
        context['suggestion'] = form.get_suggestion()

    if extra_context:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=context_class(request))
