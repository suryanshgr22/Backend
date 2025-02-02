from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
from django.core.cache import cache





class FAQ(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('bn', 'Bengali'),
    ]
    question = models.TextField()
    answer = RichTextField()
    language = models.CharField(max_length=10, default='en', choices= LANGUAGE_CHOICES )  # 'en' is the default language
    question_hi = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    

   
    
    def save(self, *args, **kwargs):
    
        short_forms = [lang[0] for lang in self.LANGUAGE_CHOICES if lang[0] != 'en']
       
        if(self.language in short_forms):
            field_name= f"question_{self.language}"
            translator = Translator()
            question = ""
            try:
                question = translator.translate(self.question, dest=self.language).text
                for lan in short_forms:
                    setattr(self,  f"question_{lan}", "")
                setattr(self, field_name, question)
            except:
                self.language = 'en'
        else:
            self.language = 'en'

        super().save(*args, **kwargs)
        self.update_cached_faqs()
    
    def update_cached_faqs(self):
        cache_key = self.language
        faqs = FAQ.objects.filter(language=cache_key) # Fetch fresh data
        cache.set(cache_key, faqs)  # Cache for 1 hour
        

    def __str__(self):
        return self.question
