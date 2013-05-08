from django import template
from django.template.loader import render_to_string
from django.conf import settings

register = template.Library()

@register.simple_tag
def contribute(*args, **kwargs):
    try:
        contact_email = settings.CONTRIBUTE_CONTACT_EMAIL
    except AttributeError:
        return ''

    subject = 'I have some info for you about a gig...'
    try:
        subject = settings.CONTRIBUTE_SUBJECT
    except AttributeError:
        pass

    rendered_string = render_to_string(
        'portal/contribute.html',
        {'contact_email': contact_email,
            'subject': subject}
    )
    return rendered_string
