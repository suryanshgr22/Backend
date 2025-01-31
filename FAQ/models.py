from django.db import models
from ckeditor.fields import RichTextField

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    language = models.CharField(max_length=10, default='en')  # 'en' is the default language
    question_hi = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    
    # Method to dynamically fetch translated question based on the requested language
    def get_translated_question(self, lang='en'):
        lang_field = f"question_{lang}"  # Construct the field name dynamically based on the language
        if hasattr(self, lang_field) and getattr(self, lang_field):
            return getattr(self, lang_field)
        return self.question  # Default to the original question if translation is not available

    def __str__(self):
        return self.question
