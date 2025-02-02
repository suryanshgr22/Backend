from ninja import NinjaAPI
from .models import FAQ
from django.core.cache import cache
from ninja.responses import Response
from django.core.exceptions import ValidationError
from .schemas import FAQSchema

app = NinjaAPI()


@app.get('faqs/', response=list[FAQSchema])
def get_faqs(request, lang: str = 'en'):
    faqs = cache.get(lang)
    if faqs:
        return faqs
    else:
        faqs = FAQ.objects.filter(language=lang)
        cache.set(lang, faqs)
    return faqs


@app.post("faqs/")
def create_faqs(request, faq: FAQSchema):
    try:
        # Validate required fields
        if not faq.question or not faq.question.strip():
            return Response({"error": "Question cannot be empty"}, status=400)

        if not faq.answer or not faq.answer.strip():
            return Response({"error": "Answer cannot be empty"}, status=400)

        # Validate language
        valid_languages = [lang[0] for lang in FAQ.LANGUAGE_CHOICES]
        if faq.language not in valid_languages:
            return Response(
                {"error": f"Invalid language. Must be one of: {', '.join(valid_languages)}"},
                status=400
            )

        # Create FAQ if validation passes
        entry = FAQ.objects.create(**faq.dict())
        return Response(
            {"message": "FAQ created successfully", "id": entry.id},
            status=201
        )
    except ValidationError as e:
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        return Response({"error": "An unexpected error occurred", "details": str(e)}, status=500)
