

class AccessChecker(object):
    """ """
    model = None
    object_field_name = None

    def get_object(self, user, obj):
        try:
            return self.model._default_manager.get(
                user=user, **{self.object_field_name: obj})
        except self.model.DoesNotExist:
            return None

    def has_access(self, user, obj, access_level):
        return False

    def get_access_level(self, user, obj):
        return 0
