from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.http import Http404, HttpResponse
from django_tablib.base import mimetype_map

from gigs.portal.datasets import ModelRelatedDataset
from gigs.gig_registry import models
from gigs.search.views import basic_search


def portal_login(request):

    error = False
    form = None

    if request.method == 'POST':
        #form = AuthenticationForm(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = None
        #if form.is_valid():
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        error = True

    form = AuthenticationForm()
    c = RequestContext(request, {'form':form, 'error': error})

    return render_to_response('portal/portal_login.html', c)


def export(request, queryset=None, model=None, headers=None, format='xls',
           filename='export'):
    if queryset is None:
        queryset = model.objects.all()

    dataset = ModelRelatedDataset(queryset)
    filename = '%s.%s' % (filename, format)
    if not hasattr(dataset, format):
        raise Http404
    response = HttpResponse(
        getattr(dataset, format),
        mimetype=mimetype_map.get(format, 'application/octet-stream')
        )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def get_gigs_data(request):
    queryset = models.Gig.objects.all()
    if request.GET.get('q', None):
        search_queryset = basic_search(request, template=None, load_all=True)
        gig_ids = [search_result.object.id for search_result in search_queryset]
        queryset = queryset.filter(pk__in=gig_ids)

    headers = [
            'venue.id',
            'venue.name',
            'venue.location.id',
            'venue.location.street_address',
            ]

    return export(request, queryset=queryset, headers=headers)

