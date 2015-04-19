from django import template
from django.forms import TextInput


class LocationWithMapWidget(TextInput):
    width = 700
    height = 200
    zoom = 16

    def render(self, name, value, attrs=None):
        tpl = '{{% load map_tags %}}' \
              '{{% render_map address {0.width} {0.height} {0.zoom} %}}'.format(self)
        map_template = template.Template(tpl)
        context = template.Context({'address': value})

        default_html = super(LocationWithMapWidget, self).render(name, value, attrs)
        return default_html + map_template.render(context)
