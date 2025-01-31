# faq/admin.py
from django.contrib import admin
from .models import FAQ
from ckeditor.widgets import CKEditorWidget
from django import forms

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'

    answer = forms.CharField(widget=CKEditorWidget())

class FAQAdmin(admin.ModelAdmin):
    form = FAQForm
    list_display = ('question', 'language', 'get_translated_question', 'answer')
    search_fields = ('question',)
    list_filter = ('language',)  # Filter FAQs by language in the admin
    ordering = ('-language',)  # Optionally order by language or any other field

    # Add a custom method to show translated question dynamically in the admin list
    def get_translated_question(self, obj):
        return obj.get_translated_question(lang=obj.language)
    get_translated_question.short_description = 'Translated Question'  # Customize column name

    # Optionally make question and answer fields editable in the list view
    list_editable = ('language',)  # Allows admins to edit the language directly in the list view

admin.site.register(FAQ, FAQAdmin)
