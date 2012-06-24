from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

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
