from django.contrib import admin

from embed_video.admin import AdminVideoMixin

from apps.geo.models import Country
from .models import Organisation


class OrganisationAdmin(AdminVideoMixin, admin.ModelAdmin):
    """
    Organisation Admin Class
    """
    autocomplete_lookup_fields = {
        'fk': ('creator', 'location',),
        'm2m': ('industries',),
    }

    fieldsets = (
        (
            None,
            {'fields': ('published', 'created', 'modified', 'expired', )}
        ),
        (
            'Recruiter Information',
            {'fields': ('creator',)}
        ),
        (
            'Basic Information',
            {'fields': ('name', 'description', 'category', 'industries', 'location', 'workforce', 'training',
                        'sponsor',)}
        ),
        (
            'Media Information',
            {'fields': ('image', 'video',)}
        ),
        (
            'Social Information',
            {'fields': ('email', 'fax', 'phone', 'mobile', 'website', 'facebook', 'twitter', 'google_plus', 'linked_in',
                        'youtube',)}
        ),
        (
            'Security Information',
            {'fields': ('country', 'established', 'registration',)}
        ),
    )
    #filter_horizontal = ('industries',)
    list_display = ('name', 'category',)
    list_per_page = 50
    raw_id_fields = ('creator', 'location', 'industries',)
    readonly_fields = ('created', 'modified', 'expired',)
    search_fields = ('name',)
    ordering = ('name',)

    class Media:
        js = ('/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              '/static/grappelli/tinymce_setup/tinymce_setup.js',)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        try:
            if db_field.name == 'country':
                kwargs['initial'] = Country.objects.get(alpha2='MU')
        except ValueError:
            pass
        return super(OrganisationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Organisation, OrganisationAdmin)
