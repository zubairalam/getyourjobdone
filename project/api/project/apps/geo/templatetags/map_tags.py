from django import template
from django.conf import settings
from django.template.loader import render_to_string
from apps.geo.models import Location

register = template.Library()


@register.tag
def render_map(parser, token):
    """
    The syntax:
        {% render_map <address> [<width> <height>] [<zoom>] [using <template_name>] %}

    The "address" parameter can be an Address instance or a string describing it.
    If an address is not found a new entry is created in the database.
    """
    width, height, zoom, template_name = None, None, None, None
    params = token.split_contents()

    # pop the template name
    if params[-2] == 'using':
        template_name = params[-1]
        params = params[:-2]

    if len(params) < 2:
        raise template.TemplateSyntaxError('render_map tag requires address argument')

    address = params[1]

    if len(params) == 4:
        width, height = params[2], params[3]
    elif len(params) == 5:
        width, height, zoom = params[2], params[3], params[4]
    elif len(params) == 3 or len(params) > 5:
        raise template.TemplateSyntaxError('render_map tag has the following syntax: '
                                           '{% render_map <address> <width> <height> [zoom] [using <template_name>] %}')
    return RenderMapNode(address, width, height, zoom, template_name)


class RenderMapNode(template.Node):
    def __init__(self, address, width, height, zoom, template_name):
        self.address = template.Variable(address)
        self.width = width or ''
        self.height = height or ''
        self.zoom = zoom or 16
        self.template_name = template.Variable(template_name or '"geo/map.html"')

    def get_map(self, address):
        if isinstance(address, Location):
            return address

        if not address:
            map_ = Location(latitude=settings.MAPS_CENTER[0],
                           longitude=settings.MAPS_CENTER[1])
        else:
            map_, _ = Location.objects.get_or_create(address=address)

        return map_


    def render(self, context):
        try:
            address = self.address.resolve(context)
            template_name = self.template_name.resolve(context)
            map_ = self.get_map(address)

            context.update({
                'map': map_,
                'width': self.width,
                'height': self.height,
                'zoom': self.zoom,
                'template_name': template_name
            })
            return render_to_string(template_name, context_instance=context)
        except template.VariableDoesNotExist:
            return ''
