from django import template
from gmapi.forms.widgets import GoogleMap

class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))
    
gmap = maps.Map(opts = {
    'center': maps.LatLng(38, -97),
    'mapTypeId': maps.MapTypeId.ROADMAP,
    'zoom': 3,
    'mapTypeControlOptions': {
    'style': maps.MapTypeControlStyle.DROPDOWN_MENU
    })
    context = {'form': MapForm(initial={'map': gmap})}
    return render_to_response('index.html', context)

class GigMapNode(template.Node):
    def __init__(self, gig):
        self.gig = template.Variable(gig)
    def render(self, context):
        try:
            gig = self.gig.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        
def do_gig_map(parser, token):

    try:
        tag_name, gig = token.split_context()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires 1 argument' % 
                token.contents.split()[0])

    return GigMapNode(gig)
