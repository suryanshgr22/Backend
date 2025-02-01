from ninja import NinjaAPI
from .models import FAQ
from .schemas import FAQSchema
from googletrans import Translator

app = NinjaAPI()

@app.get('faqs/', response=list[FAQSchema])
def get_faqs(request, lang : str = 'en'):
    faqs = FAQ.objects.filter(language = lang)
    return faqs

# @app.post('faqs/')
# def get_faqs(request):
    
#     return 