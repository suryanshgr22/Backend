from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator

LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('hi', 'Hindi'),
    ('bn', 'Bengali')
]



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
        # print(self.language)
        short_forms = [lang[0] for lang in LANGUAGE_CHOICES].remove('en')
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
        return
        

    def __str__(self):
        return self.question
