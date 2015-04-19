import requests
import json
import uuid

import hashlib
import facebook

#from apps.accounts.models import (User, UserProfile, FacebookProfile,
#                                  FacebookUserLocation, FacebookEducationHistory, FacebookWorkHistory,
#                                  LinkedInProfile, LinkedInEducationHistory, LinkedInWorkHistory)
#

from apps.accounts.models import User, UserProfile

from .models import (FacebookProfile, FacebookUserLocation, FacebookEducationHistory, FacebookWorkHistory,
                        LinkedInProfile, LinkedInEducationHistory, LinkedInWorkHistory)

from apps.core.helpers import image_downloader


class Profile(object):
    @staticmethod
    def create_user_profile(user, profile):
        # returns true if user_profile created or if it exists
        # else returns false

        created = False
        try:
            user_profile = UserProfile.objects.get(user=user)
            created = True
        except:
            first_name = profile.get('first_name', '')
            last_name = profile.get('last_name', '')
            birthday = profile.get('birthday', '')
            gender = profile.get('gender', '')

            if gender != "":
                if gender.lower() == "male":
                    gender = 1
                elif gender.lower() == "female":
                    gender = 2
                else:
                    gender = 3
            md5_hexed_email = hashlib.md5(user.email.encode('utf-8')).hexdigest()
            avatar = 'https://secure.gravatar.com/avatar/{0}?default=identicon'.format(md5_hexed_email)
            # download profile image
            filename = "{}{}{}".format('images/users/', uuid.uuid4(), '.jpg')
            image_downloader(profile.get('profile_pic'), filename)
            user_profile = UserProfile.objects.create(user=user, first_name=first_name, last_name=last_name,
                                                      birthday=birthday, avatar=avatar, image=filename)
            if gender != "":
                user_profile.gender = gender
                user_profile.save()
            created = True
        return created

    @staticmethod
    def update_facebook_data(user, profile):
        # updates facebook user profile
        pass

    @staticmethod
    def update_facebook_profile_pic(user, profile):
        pass

    @staticmethod
    def create_facebook_profile(user, profile):
        # if facebook_profile exists or created return true
        # else return false
        # creates facebook_education_history
        # facebook_work_history
        # facebook_user_location
        created = False
        try:
            fb_profile = FacebookProfile.objects.get(user=user)
            Profile.update_facebook_data(user, profile)
            created = True
        except:
            first_name = profile.get('first_name', '')
            last_name = profile.get('last_name', '')
            birthday = profile.get('birthday', '')
            gender = profile.get('gender', '')
            profile_id = profile.get('id', '')
            website = profile.get('website', '')
            if gender != "":
                if gender == "male":
                    gender = 1
                elif gender == "female":
                    gender = 2
                else:
                    gender = 3
            md5_hexed_email = hashlib.md5(user.email.encode('utf-8')).hexdigest()
            avatar = 'https://secure.gravatar.com/avatar/{0}?default=identicon'.format(md5_hexed_email)
            profile_pic = profile["profile_pic"]

            facebook_profile = FacebookProfile.objects.create(user=user,
                                                              first_name=first_name,
                                                              last_name=last_name,
                                                              birthday=birthday,
                                                              avatar=avatar,
                                                              profile_pic=profile_pic,
                                                              profile_id=profile_id,
                                                              website=website)
            if gender != "":
                facebook_profile.gender = gender
                facebook_profile.save()
            created = True

            # facebook user location details
            try:
                location_id = profile["location"]["id"]
                location_name = profile["location"]["name"]
                user_location = FacebookUserLocation(location_id=location_id, location_name=location_name)
                facebook_profile.location = user_location
                facebook_profile.save()
            except:
                pass


            # facebook educational history
            if profile.get('education', '') != "":
                for education in profile["education"]:
                    valid_edu = False
                    try:
                        school_id = education["school"]["id"]
                        school_name = education["school"]["name"]
                        valid_edu = True
                    except:
                        school_id = ""
                        school_name = ""
                    institute_type = education.get('type', '')
                    try:
                        year_id = education["year"]["id"]
                        year_name = education["year"]["name"]
                        valid_edu = True
                    except:
                        year_id = ""
                        year_name = ""
                    try:
                        degree_id = education["degree"]["id"]
                        degree_name = education["degree"]["name"]
                        valid_edu = True
                    except:
                        degree_id = ""
                        degree_name = ""
                    if valid_edu:
                        facebook_profile.education_history.create(school_id=school_id,
                                                                  school_name=school_name,
                                                                  institute_type=institute_type,
                                                                  degree_id=degree_id,
                                                                  degree_name=degree_name,
                                                                  year_id=year_id,
                                                                  year_name=year_name)
            if profile.get('work', '') != "":
                # facebook work history
                for work in profile['work']:
                    valid_work = False
                    try:
                        employer_id = work["employer"]["id"]
                        employer_name = work["employer"]["name"]
                        valid_work = True
                    except:
                        employer_id = ""
                        employer_name = ""
                    try:
                        location_id = work["location"]["id"]
                        location_name = work["location"]["name"]
                        valid_work = True
                    except:
                        location_id = ""
                        location_name = ""
                    try:
                        position_id = work["position"]["id"]
                        position_name = work["position"]["name"]
                        valid_work = True
                    except:
                        position_id = ""
                        position_name = ""
                    start_date = work.get('start_date', '')
                    if valid_work:
                        facebook_profile.work_history.create(employer_id=employer_id,
                                                             employer_name=employer_name,
                                                             location_id=location_id,
                                                             location_name=location_name,
                                                             position_id=position_id,
                                                             position_name=position_name,
                                                             start_date=start_date)

        return created

    @staticmethod
    def get_linkedin_profile(user, token):
        fields = (":(first_name,last_name,email-address,picture-url,date-of-birth,"
                  "phone-numbers,public-profile-url,positions,educations,skills,location)?oauth2_access_token=")
        url = '{}{}{}&format=json'.format('https://api.linkedin.com/v1/people/~', fields, token)

        response = requests.get(url)
        profile = json.loads(response.text)

        # save image to users folder first
        filename = '{}{}.jpg'.format('images/users/', uuid.uuid4())
        image_downloader(profile.get('pictureUrl'), filename)

        # activate user account
        user.active = True
        user.save()

        # create local user profile
        UserProfile.objects.create(user=user,
                                   first_name=profile.get('firstName', ''),
                                   last_name=profile.get('lastName', ''),
                                   birthday=profile.get('dateOfBirth', ''),
                                   image=filename
        )

        # create linkedin_profile
        linkedin_profile = LinkedInProfile.objects.create(user=user,
                                                          first_name=profile.get('firstName', ''),
                                                          last_name=profile.get('lastName', ''),
                                                          birthday=profile.get('dateOfBirth', ''),
                                                          image=filename,
        )

        # create linkedin work history
        if profile.get('positions', '') != '':
            jobs = profile['positions']['values']
            for job in jobs:
                end_date_month = ''
                end_date_year = ''
                if not job.get('isCurrent'):
                    end_date_month = job['endDate']['month']
                    end_date_year = job['endDate']['year']

                start_date_month = ''
                start_date_year = ''
                if job.get('startDate', '') != '':
                    start_date_month = job['startDate']['month']
                    start_date_year = job['startDate']['year']
                company = ''
                if job.get('company', '') != '':
                    company = job['company']['name']

                linkedin_profile.work_history.create(company=company,
                                                     company_id=job.get('id', ''),
                                                     is_current=job.get('isCurrent', ''),
                                                     start_date_year=start_date_year,
                                                     start_date_month=start_date_month,
                                                     end_date_year=end_date_year,
                                                     end_date_month=end_date_month,
                                                     summary=job.get('summary', ''),
                                                     title=job.get('title', '')
                )

        # create linkedin education history
        if profile.get('educations', '') != '':
            edus = profile['educations']['values']
            for edu in edus:
                end_date_year = ''
                if edu.get('endDate', '') != '':
                    end_date_year = edu['endDate']['year']
                start_date_year = ''
                if edu.get('startDate', '') != '':
                    start_date_year = edu['startDate']['year']
                linkedin_profile.education_history.create(
                    activities=edu.get('activities', ''),
                    start_date_year=start_date_year,
                    end_date_year=end_date_year,
                    field_of_study=edu.get('fieldOfStudy', ''),
                    degree_id=edu.get('id', ''),
                    degree=edu.get('degree'''),
                    notes=edu.get('notes', ''),
                    school_name=edu.get('schoolName', '')
                )
        # create linkedin skills
        if profile.get('skills', '') != "":
            skills = profile['skills']['values']
            for skill in skills:
                skill_id = skill['id']
                skill = skill['skill']['name']
                sk = linkedin_profile.skills.create(skill_id=skill_id, skill=skill)

    @staticmethod
    def get_facebook_profile(user, token):
        # use facebook app
        # all that need is a token
        # and call all those functions from here
        graph = facebook.GraphAPI(token)

        profile = graph.get_object("me")
        pictures = graph.get_connections("me", "picture")
        profile_pic = pictures.get('url', '')
        profile["profile_pic"] = profile_pic

        # activate user account
        user.active = True
        user.save()
        Profile.create_user_profile(user, profile)
        Profile.create_facebook_profile(user, profile)


    @staticmethod
    def update_profile(user):
        # This will update local profile, linkedin or facebook profile
        pass

    @staticmethod
    def create_social_profile(provider, user, token):
        assert (provider and user and token)
        profile_providers = {'linkedin_oauth2': Profile.get_linkedin_profile, 'facebook': Profile.get_facebook_profile}
        profile_providers[provider.lower()](user, token)

