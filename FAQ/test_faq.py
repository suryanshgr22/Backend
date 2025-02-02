import pytest
from django.core.cache import cache
from .models import FAQ
import json
from unittest.mock import patch


# Fixtures
@pytest.fixture(autouse=True)
def clear_cache():
    """Automatically clear cache before and after each test"""
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def faq_data():
    """Base FAQ data fixture"""
    return {
        'question': 'What is a test question?',
        'answer': '<p>This is a test answer.</p>',
        'language': 'en'
    }


@pytest.fixture
def api_client():
    """Django test client fixture"""
    from django.test import Client
    return Client()


# Model Tests
@pytest.mark.django_db
class TestFAQModel:
    def test_create_faq_english(self, faq_data):
        faq = FAQ.objects.create(**faq_data)
        assert faq.question == 'What is a test question?'
        assert faq.language == 'en'
        assert faq.question_hi is None
        assert faq.question_bn is None

    @pytest.mark.parametrize('lang,translated_text', [
        ('hi', 'यह एक परीक्षण प्रश्न है'),
        ('bn', 'এটি একটি পরীক্ষার প্রশ্ন')
    ])
    def test_create_faq_translations(self, faq_data, lang, translated_text):
        with patch('googletrans.Translator.translate') as mock_translate:
            mock_translate.return_value.text = translated_text

            faq_data['language'] = lang
            faq = FAQ.objects.create(**faq_data)

            field_name = f'question_{lang}'
            assert getattr(faq, field_name) == translated_text
            mock_translate.assert_called_once()

    def test_translation_failure_fallback(self, faq_data):
        faq_data['language'] = 'hi'

        with patch('googletrans.Translator.translate', side_effect=Exception('Translation failed')):
            faq = FAQ.objects.create(**faq_data)
            assert faq.language == 'en'

    def test_cache_update(self, faq_data):
        FAQ.objects.create(**faq_data)
        cached_faqs = cache.get('en')
        assert cached_faqs is not None
        assert len(cached_faqs) == 1

    @pytest.mark.parametrize('invalid_lang', ['fr', 'es', 'invalid'])
    def test_invalid_language_fallback(self, faq_data, invalid_lang):
        faq_data['language'] = invalid_lang
        faq = FAQ.objects.create(**faq_data)
        assert faq.language == 'en'


# API Tests
@pytest.mark.django_db
class TestFAQAPI:
    def test_get_faqs_empty(self, api_client):
        response = api_client.get('/api/faqs/')
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_get_faqs_with_data(self, api_client, faq_data):
        FAQ.objects.create(**faq_data)

        # First request - should hit database
        response = api_client.get('/api/faqs/')
        assert response.status_code == 200
        assert len(response.json()) == 1

        # Second request - should hit cache
        with patch('django.db.models.query.QuerySet.filter') as mock_filter:
            response = api_client.get('/api/faqs/')
            assert response.status_code == 200
            mock_filter.assert_not_called()

    @pytest.mark.parametrize('test_data,expected_status', [
        ({'question': 'Valid question?', 'answer': '<p>Answer</p>', 'language': 'en'}, 201),
        ({'question': '', 'answer': '<p>Answer</p>', 'language': 'en'}, 400),
        ({'question': 'Question?', 'answer': '', 'language': 'en'}, 400),
        ({'question': 'Question?', 'answer': '<p>Answer</p>', 'language': 'invalid'}, 400),
    ])
    def test_create_faq(self, api_client, test_data, expected_status):
        response = api_client.post(
            '/api/faqs/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        assert response.status_code == expected_status
        if expected_status == 201:
            assert 'id' in response.json()
            assert FAQ.objects.count() == 1

    @pytest.mark.parametrize('lang', ['en', 'hi', 'bn'])
    def test_get_faqs_different_languages(self, api_client, faq_data, lang):
        # Create FAQ in specified language
        with patch('googletrans.Translator.translate') as mock_translate:
            mock_translate.return_value.text = f'Translated to {lang}'
            faq_data['language'] = lang
            FAQ.objects.create(**faq_data)

        response = api_client.get(f'/api/faqs/?lang={lang}')
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_cache_invalidation(self, api_client, faq_data):
        # Create initial FAQ
        FAQ.objects.create(**faq_data)

        # First request
        response = api_client.get('/api/faqs/')
        initial_data = response.json()

        # Create another FAQ
        new_faq = faq_data.copy()
        new_faq['question'] = 'Another question?'
        FAQ.objects.create(**new_faq)

        # Second request
        response = api_client.get('/api/faqs/')
        updated_data = response.json()

        assert len(updated_data) == 2
        assert initial_data != updated_data


# Integration Tests
@pytest.mark.django_db
class TestFAQIntegration:
    def test_create_and_retrieve_workflow(self, api_client, faq_data):
        # Create FAQ
        response = api_client.post(
            '/api/faqs/',
            data=json.dumps(faq_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        response.json()['id']

        # Retrieve FAQ
        response = api_client.get('/api/faqs/')
        data = response.json()
        assert len(data) == 1
        assert data[0]['question'] == faq_data['question']

        # Verify cache
        cached_faqs = cache.get('en')
        assert cached_faqs is not None
        assert len(cached_faqs) == 1
