from django.db.models.enums import ChoicesMeta
from . import SetEnumMeta

class DjangoChoicesSetEnumMeta(SetEnumMeta, ChoicesMeta):
    pass
