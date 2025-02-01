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
    list_display = ('question', 'language', 'answer')
    search_fields = ('question',)
    list_filter = ('language',)  # Filter FAQs by language in the admin
    list_editable = ('language',)  # Allows admins to edit the language directly in the list view

admin.site.register(FAQ, FAQAdmin)
