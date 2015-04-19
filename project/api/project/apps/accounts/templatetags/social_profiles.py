from django import template
register = template.Library()

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from apps.profile.models import LinkedInProfile, LinkedInWorkHistory, LinkedInEducationHistory

@register.filter(name='get_linkedin_work_history')
def get_linkedin_work_history(user):
	try:
		in_profile = LinkedInProfile.objects.get(user=user)
		return in_profile.work_history.values()
	except ObjectDoesNotExist:
		pass
	return None

@register.filter(name='get_linkedin_education_history')
def get_linkedin_education_history(user):
	try:
		in_profile = LinkedInProfile.objects.get(user=user)
		return in_profile.education_history.values()
	except ObjectDoesNotExist:
		pass
	return None

@register.filter(name='get_basic_profile')
def get_basic_profile(user):
	try:
		in_profile = LinkedInProfile.objects.get(user=user)
		return in_profile
	except ObjectDoesNotExist:
		pass
	return None
