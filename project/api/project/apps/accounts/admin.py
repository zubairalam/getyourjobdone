from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.forms import models

from .forms import UserChangeForm, UserCreationForm
from .models import User, UserAccount, UserReferral, UserRelationship, UserProfile, UserSetting
# from .models import User, UserReferral, UserRelationship, UserProfile, UserSetting


class UserInlineFormSet(models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(UserInlineFormSet, self).__init__(*args, **kwargs)
        self.can_delete = False


class UserAccountInline(admin.StackedInline):
   formset = UserInlineFormSet
   inline_classes = ('grp-collapse grp-open',)
   model = UserAccount
   max_num = 1
   extra = 1

# class UserAccountInline(admin.StackedInline):
#     formset = UserInlineFormSet
#     inline_classes = ('grp-collapse grp-open',)
#     model = User
#     max_num = 1
#     extra = 1


class UserProfileInline(admin.StackedInline):
    formset = UserInlineFormSet
    inline_classes = ('grp-collapse grp-open',)
    model = UserProfile
    max_num = 1
    extra = 1


class UserSettingInline(admin.StackedInline):
    formset = UserInlineFormSet
    inline_classes = ('grp-collapse grp-open',)
    model = UserSetting
    max_num = 1
    extra = 1


class UserAdmin(BaseUserAdmin):
    """
    User Admin Class
    """


    def picture_tag(self):
        return u'<img src=\"%s\" height=\"80\" width=\"80\" />' % self.get_picture()

    picture_tag.short_description = 'Picture'
    picture_tag.allow_tags = True

    def name(self):
        return self.get_full_name()

    #def account(self):
    #    from .choices import UserAccountTypeChoices

    #    return UserAccountTypeChoices[self.get_account().account]

    name.short_description = 'Name'

    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2',), }),
    )
    fieldsets = (
        (None, {'classes': ('placeholder user_account-group',), 'fields': ()}),
        ('Personal Info', {'fields': ('email', 'password', 'hash', picture_tag, )},),
        (None, {'classes': ('placeholder user_profile-group',), 'fields': ()}),
        (None, {'classes': ('placeholder user_setting-group',), 'fields': ()}),
        ('User Permissions', {'fields': ('active', 'is_staff', 'is_superuser', 'terms',)},),
        ('Important Dates', {'fields': ('created', 'last_login',)},),
    )
    add_form = UserCreationForm
    form = UserChangeForm
    inlines = (UserProfileInline, UserAccountInline, UserSettingInline, )
    inlines = (UserProfileInline, UserSettingInline, )
    list_per_page = 50
    #list_display = (picture_tag, name, 'email', account, 'created', 'last_login', 'active',)
    list_display = (picture_tag, name, 'email', 'created', 'last_login', 'active',)
    list_display_links = (picture_tag, name)
    list_filter = ('active', 'created', 'last_login',)
    readonly_fields = (picture_tag, 'created', 'last_login', 'hash',)
    search_fields = ('email',)
    ordering = ('email',)

    class Media:
        js = ('/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              '/static/grappelli/tinymce_setup/tinymce_setup.js',)


admin.site.register(User, UserAdmin)


class UserAccountAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    list_per_page = 50
    raw_id_fields = ('user',)


admin.site.register(UserAccount, UserAccountAdmin)

admin.site.unregister(Group)
admin.site.register(UserReferral)

admin.site.register(UserRelationship)
