from django.contrib import admin

from .models import Industry, Language, License, Membership, Skill, Qualification, WorkExperience


class IndustryAdmin(admin.ModelAdmin):
    """
    Industry Admin Class
    """
    fields = ('name', 'parent',)
    list_display = ('name', 'parent', 'slug',)
    list_per_page = 50
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Industry, IndustryAdmin)


class LanguageAdmin(admin.ModelAdmin):
    """
    Language Admin Class
    """
    fields = ('name',)
    list_display = ('name', 'slug',)
    list_per_page = 50
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Language, LanguageAdmin)


class LicenseAdmin(admin.ModelAdmin):
    """
    License Admin Class
    """
    fields = ('name',)
    list_display = ('name', 'slug',)
    list_per_page = 50
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(License, LicenseAdmin)


class MembershipAdmin(admin.ModelAdmin):
    """
    Membership Admin Class
    """
    fields = ('name',)
    list_display = ('name', 'slug',)
    list_per_page = 50
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Membership, MembershipAdmin)


class SkillAdmin(admin.ModelAdmin):
    """
    Skill Admin Class
    """
    fields = ('name',)
    list_display = ('name', 'slug',)
    list_per_page = 50
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Skill, SkillAdmin)
