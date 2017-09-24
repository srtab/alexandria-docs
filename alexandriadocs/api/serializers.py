from projects.models import ImportedArchive
from rest_framework import serializers


class ImportedArchiveSerializer(serializers.ModelSerializer):
    """ """
    class Meta:
        model = ImportedArchive
        fields = ('project', 'archive')
