class BaseCustomChoiceField(object):
    """
    Base class for a custom choice field that can provide a default queryset.
    """

    def __init__(self, *args, **kwargs):
        kwargs['queryset'] = self.provide_queryset()
        super(BaseCustomChoiceField, self).__init__(*args, **kwargs)

    def provide_queryset(self):
        """
        Allow a child field to override the default queryset of the choice field.
        """
        raise NotImplementedError
