from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from gigs.gig_registry import models

from django_tablib import models as tablib_models
from django_tablib import views as tablib_views

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

class GigDataset(tablib_models.ModelDataset):
    class Meta:
        #queryset = models.Gig.objects.filter(is_aw
        model = models.Gig


def get_gigs_data(request):
    gigs_ids_string = request.GET.get('ids', '')
    gig_ids = gigs_ids_string.split(',')
    queryset = models.Gig.objects.all()
    if gig_ids:
        queryset = queryset.filter(pk__in=gig_ids)
    return tablib_views.export(request, queryset=queryset)

