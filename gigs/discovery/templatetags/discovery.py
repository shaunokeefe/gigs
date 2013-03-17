from datetime import date

from django import template
from django.template.loader import render_to_string
from django.contrib.admin import models as admin_models
from django.db.models import get_app, get_models
from django.conf import settings

register = template.Library()
# TODO
# Panel to choose n random panels
#


@register.simple_tag
def on_this_day(model_name, **kwargs):
    today = date.today()
    number_of_decades = kwargs.get('num_decades', 6)

    model = None
    for app_name in settings.DISCOVERY_APPS:
        app = get_app(app_name)
        for m in get_models(app):
            if m.__name__.lower() != model_name:
                continue
            model = m

    if not model:
        return ''

    todays_entries = model.objects.\
        filter(start__day=today.day, start__month=today.month).\
        order_by('?')
    this_months_entries = model.objects.\
        filter(start__month=today.month).\
        order_by('?')
    yearly_entries = {}
    for year in range(10, number_of_decades * 10, 10):
        entries = model.objects.\
            filter(start__year=today.year - year).\
            order_by('?')
        if entries:
            yearly_entries[year] = entries
    weekdays = model.objects.\
        filter(start__week_day=today.weekday).\
        order_by('?')
    rendered_string = render_to_string(
        'discovery/on_this_day.html',
        {
            'today': todays_entries,
            'this_month': this_months_entries,
            'past_decades': yearly_entries,
            'weekdays': weekdays,
        }
    )
    return rendered_string


@register.simple_tag
def random(model_name, **kwargs):
    model = None
    for app_name in settings.DISCOVERY_APPS:
        app = get_app(app_name)
        for m in get_models(app):
            if m.__name__.lower() != model_name:
                continue
            model = m

    if not model:
        return ''
    entry = model.objects.order_by('?')[0]
    rendered_string = render_to_string(
        'discovery/random.html',
        {'entry': entry}
    )
    return rendered_string


@register.simple_tag
def recent_edits(*args, **kwargs):
        model = kwargs.get('model', None)
        num_edits = kwargs.get('num_edits', 1)
        if not model:
            try:
                models = settings.DISCOVERY_MODELS
            except AttributeError:
                models = []
        else:
            models = [model]
        recent_edits = admin_models.LogEntry.objects.\
            filter(content_type__model__in=models).\
            order_by('?')[:num_edits]
        rendered_string = render_to_string(
            'discovery/recent_edits.html',
            {'recent_edits': recent_edits}
        )
        return rendered_string
