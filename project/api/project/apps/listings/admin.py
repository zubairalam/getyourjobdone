from django.contrib import admin

from .models import Course, Tuition, Job, JobResponsibility, JobBenefit, Project


class ListingAdmin(admin.ModelAdmin):
    """
    Abstract Listing Model Admin Class.
    """

    def picture_tag(self):
        return u'<img src="%s" height="80" width="80" />' % self.image

    picture_tag.short_description = 'Course Image'
    picture_tag.allow_tags = True
    fieldsets = (
        (
            None,
            {'fields': ('published', 'created', 'modified', 'expired', 'reference', )}
        ),
        (
            'Advertiser',
            {'fields': ('creator',)},),
        (
            'Information',
            {'fields': (
                'name', 'description', 'category', 'days', 'industry', 'location', 'experience', 'qualification',
                'languages', 'licenses', 'memberships', 'skills',
                'duration_count', 'duration_time', 'date_start', 'time_start', 'time_end',  )},
        ),
        (
            'Media Information',
            {'fields': ('image', 'video',)}
        ),
    )
    list_per_page = 50
    list_display = (picture_tag, 'name', 'category', 'industry',)
    list_display_links = (picture_tag,)
    raw_id_fields = ('creator',)
    readonly_fields = ('created', 'modified', 'expired',)
    search_fields = ('name',)
    ordering = ('name',)


class CourseAdmin(ListingAdmin):
    """
    Course Admin Class.
    """
    fieldsets = ListingAdmin.fieldsets + (('More', {
        'fields': (
            'level', 'price', 'price_retail', 'price_frequency', 'price_negotiable', 'awarded', 'achievement',)}),)


admin.site.register(Course, CourseAdmin)


class TuitionAdmin(ListingAdmin):
    """
    Tuition Admin Class.
    """
    fieldsets = ListingAdmin.fieldsets + (('More', {
        'fields': ('level', 'price', 'price_retail', 'price_frequency', 'price_negotiable',)}),)


admin.site.register(Tuition, TuitionAdmin)


class ProjectAdmin(ListingAdmin):
    """
    Project Admin Class.
    """
    fieldsets = ListingAdmin.fieldsets + (('More', {'fields': ('price', 'price_negotiable',)}),)


admin.site.register(Project, ProjectAdmin)


class JobBenefitInline(admin.TabularInline):
    model = JobBenefit
    extra = 1
    max_num = 3


class JobResponsibilityInline(admin.TabularInline):
    model = JobResponsibility
    extra = 2
    max_num = 10


class JobAdmin(admin.ModelAdmin):
    """
    Job Admin Class.
    """
    fieldsets = ListingAdmin.fieldsets + (('More', {'fields': (
        'police_record', 'work_permit', 'work_environment', 'salary_min', 'salary_max', 'salary_frequency',
        'salary_negotiable',)}),)
    inlines = (JobBenefitInline, JobResponsibilityInline)


admin.site.register(Job, JobAdmin)