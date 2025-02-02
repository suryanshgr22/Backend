from ninja import NinjaAPI
from .models import FAQ
from .schemas import FAQSchema
from googletrans import Translator
from django.core.cache import cache
from ninja.responses import Response
from django.core.exceptions import ValidationError

app = NinjaAPI()

@app.get('faqs/', response=list[FAQSchema])
def get_faqs(request, lang : str = 'en'):
    faqs = cache.get(lang)
    if(faqs):
        print('from cache')
        return faqs
    else:
        print('from DB')
        faqs = FAQ.objects.filter(language = lang)
        cache.set(lang, faqs)
    return faqs

@app.post("faqs/")
def create_faqs(request, faq: FAQSchema):
    try:
        entry = FAQ.objects.create(**faq.dict())  # Convert Schema to dictionary
        return Response(
            {"message": "FAQ created successfully", "id": entry.id}, 
            status=201 
        )
    except ValidationError as e:
        return Response({"error": str(e)}, status=400)  # 400 for invalid data
    except Exception as e:
        return Response({"error": "An unexpected error occurred", "details": str(e)}, status=500)