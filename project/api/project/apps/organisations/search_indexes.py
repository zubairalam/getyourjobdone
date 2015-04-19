from haystack import indexes

from .models import Organisation


class OrganisationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    creator = indexes.CharField(model_attr='creator', faceted=True)
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return Organisation

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.all()