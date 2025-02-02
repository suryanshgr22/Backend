from .models import FAQ
from ninja import ModelSchema


class FAQSchema(ModelSchema):
    class Meta:
        model = FAQ
        fields = ('id', 'question', 'answer', 'language', 'question_hi', 'question_bn')

