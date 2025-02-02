# Backend for BharatFD

This is the backend service for BharatFD, built using Django and Django Ninja for API development. It provides API endpoints for managing FAQs with multi-language support, caching, and efficient data retrieval.

## Features
- **Django Ninja API**: Fast and easy API development.
- **Multi-language FAQ Support**: Automatically translates FAQs using Google Translate.
- **Caching**: Uses Django's caching system for improved performance.
- **Rich Text Support**: CKEditor integration for rich-text answers.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.10+
- pip

### Setup Instructions

1. **Clone the repository**
   ```sh
   git clone https://github.com/suryanshgr22/Backend.git
   cd Backend
   ```

2. **Create a virtual environment** (recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the database**
   Update `settings.py` with your database credentials and then run:
   ```sh
   python manage.py migrate
   ```

5. **Run the development server**
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### 1. Get FAQs
- **Endpoint**: `GET /faqs/`
- **Parameters**:
  - `lang` (query param) - Language code (`en`, `hi`, `bn`)
- **Response**:
  ```json
  [
    {
      "question": "What is BharatFD?",
      "answer": "BharatFD is a platform for...",
      "language": "en"
    }
  ]
  ```

### 2. Create FAQ
- **Endpoint**: `POST /faqs/`
- **Request Body**:
  ```json
  {
    "question": "What is BharatFD?",
    "answer": "BharatFD is a platform for...",
    "language": "en"
  }
  ```
- **Response**:
  ```json
  {
    "message": "FAQ created successfully",
    "id": 1
  }
  ```

## Running Tests
We use `pytest` for testing. Run tests with:
```sh
pytest
```

If pytest isn't recognized, try:
```sh
python -m pytest
```

### Configure `pytest-django`
Ensure you have `pytest-django` installed and set up the correct settings module:
```sh
pip install pytest-django
```
Add a `pytest.ini` file:
```ini
[pytest]
DJANGO_SETTINGS_MODULE = Backend.settings
```

## Contribution Guidelines
1. Fork the repository.
2. Create a new branch (`feature-xyz`).
3. Commit your changes.
4. Push to your branch and submit a pull request.

## License
MIT License

