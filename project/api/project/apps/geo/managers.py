from django.db import models
import pycountry


class BaseCountryManager(models.Manager):
    """
    Base manager for any model that shadows a pycountry database.
    """

    def sync(self):
        """"
        Syncs the managed model with its pycountry equivalent.
        """

        model_fields = self.model._meta.get_all_field_names()

        # Clear all existing model instances
        self.all().delete()

        # Create a new model instance for every datum in the pycountry database
        for resource in self.provide_pycountry_database():
            kwargs = {}
            for field_name in model_fields:
                if hasattr(resource, field_name):
                    kwargs[field_name] = getattr(resource, field_name)
            self.create(**kwargs)

    def provide_pycountry_database(self):
        """
        Provide the pycountry database that the model shadows.
        """
        raise NotImplementedError


class CountryManager(models.Manager):
    """
    Custom manager for the Country model.
    """

    def get_by_natural_key(self, alpha3):
        return self.get(alpha3=alpha3)


class CustomCountryManager(BaseCountryManager):
    """
    Pycountry manager for the Country model.
    """

    def provide_pycountry_database(self):
        return pycountry.countries