from import_export import resources
from .models import survey

class SurveyResource(resources.ModelResource):
    class Meta:
        model = Survey