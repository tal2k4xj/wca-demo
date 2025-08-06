# WCA I18N - Multilingual Code Explanation API

A FastAPI service that provides code explanations in multiple languages using Watson Code Assistant.

[Owner Contact](https://ibm.enterprise.slack.com/archives/D08EJANBT8A)

## Features

- Code explanation in multiple languages:
  - Traditional Chinese (繁體中文)
  - Simplified Chinese (简体中文)
  - Korean (한국어)
  - Thai (ภาษาไทย)
  - Indonesian (Bahasa Indonesia)
  - Vietnamese (Tiếng Việt)
  - English (default)

- Natural language explanations with:
  - Main functionality description
  - Implementation principles
  - Parameter and return value explanations
  - Real-life examples for algorithms and design patterns

## Project Structure 

```
root/
├── backend/
│   ├── __init__.py
│   ├── wca_i18n.py      # Main FastAPI application
│   ├── wca_backend.py   # Backend logic and AI integration
│   ├── requirements.txt # Project dependencies
│   └── tests/          # Test suite
│       ├── __init__.py
│       └── test_api.py
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd wca-i18n
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.template` to `.env`
   - Add your API keys and configuration:
```
API_KEY=your_api_key_here
IAM_APIKEY=your_iam_apikey_here
PROJECT_ID=your_project_id
IAM_IBM_CLOUD_URL=iam.cloud.ibm.com
```

## API Endpoints

### Health Check
- `GET /health` - Check service health status

### Chat
- `POST /chat` - Process code analysis requests
  ```json
  {
      "message": "Please explain this code",
      "code": "your_code_here"
  }
  ```

### Code Explanation
- `POST /explain/{language}` - Explain code in specific language
  ```json
  {
      "code": "your_code_here"
  }
  ```

Available language options:
- `traditional_chinese`
- `simplified_chinese`
- `korean`
- `thai`
- `indonesian`
- `vietnamese`
- `english`

## Testing

Run the test suite:
```bash
# Run all tests
pytest backend/tests/

# Run with output visible
pytest -s backend/tests/
```

## Error Handling

The API provides appropriate error messages in the respective languages for:
- Empty code submissions
- Authentication failures
- API errors
- Invalid requests

## Development

### Prerequisites
- Python 3.x
- FastAPI
- IBM Watson API credentials

### Best Practices
- Follow PEP 8 style guide
- Write tests for new features
- Document API changes
- Handle errors gracefully
- Use appropriate language detection
- Maintain consistent response formats

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the tests
5. Submit a pull request

## License

[Your License Here]

## Overview

This service provides API endpoints for:
- Multi-language code analysis and explanations
- File upload and processing
- Vector database querying
- Support for multiple programming languages
- PDF file processing

## Project Structure 

```
root/
├── backend/
│   ├── __init__.py
│   ├── wca_i18n.py      # Main FastAPI application
│   ├── wca_backend.py   # Backend logic and AI integration
│   ├── requirements.txt # Project dependencies
│   └── tests/          # Test suite
│       ├── __init__.py
│       └── test_api.py
```

## API Endpoints

### Health Check
- `GET /health` - Check service health status

### Chat
- `POST /chat` - Process code analysis requests
  - Request body:
    ```json
    {
        "message": "string",
        "code": "string"
    }
    ```

### Code Explanation in Different Languages
- `POST /explain/traditional` - Traditional Chinese (繁體中文) explanation
- `POST /explain/simplified` - Simplified Chinese (简体中文) explanation
- `POST /explain/korean` - Korean (한국어) explanation
- `POST /explain/japanese` - Japanese (日本語) explanation
- `POST /explain/hindi` - Hindi (हिंदी) explanation
- `POST /explain/thai` - Thai (ไทย) explanation
- `POST /explain/indonesian` - Indonesian (Bahasa Indonesia) explanation
- `POST /explain/vietnamese` - Vietnamese (Tiếng Việt) explanation
  - Request body:
    ```json
    {
        "code": "string"
    }
    ```
  - Response format for all language endpoints:
    ```json
    {
        "explanation": "string",
        "analysis": ["string"]
    }
    ```

### File Operations
- `POST /upload` - Upload files for processing
  - Supports: Python, Java, JavaScript, CSS, HTML, SQL, PDF files
- `GET /files` - Get file processing status

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Set up environment variables:
   ```bash
   export API_KEY=your_ibm_api_key
   export PROJECT_ID=your_project_id
   ```
4. Run the application:
   ```bash
   uvicorn backend.wca_i18n:app --reload
   ```

## Testing

Run the test suite:

```bash
# Run all tests
pytest backend/tests/test_api.py

# Run with output visible
pytest backend/tests/test_api.py -s

# Run specific test with verbose output
pytest backend/tests/test_api.py::test_name -sv
```

## Features

### Multi-language Support
- Traditional Chinese (繁體中文)
- Simplified Chinese (简体中文)
- Korean (한국어)
- Japanese (日本語)
- Hindi (हिंदी)
- Thai (ไทย)
- Indonesian (Bahasa Indonesia)
- Vietnamese (Tiếng Việt)
- English (default)

### Code Analysis
- Multi-language support:
  - Python
  - Java
  - JavaScript
  - CSS
  - HTML
  - SQL

### File Processing
- Support for:
  - Individual code files
  - Multiple file uploads
  - ZIP archives
  - PDF documents

### Vector Database Integration
- Context-aware responses
- Code similarity search
- Intelligent query processing

## Error Handling

The API implements comprehensive error handling for:
- Invalid requests
- Empty code submissions
- File processing errors
- Resource limitations
- Concurrent operation issues

## Development

### Prerequisites
- Python 3.x
- FastAPI
- IBM Watson API credentials
- Vector database setup
- PDF processing capabilities

### Best Practices
- Follow PEP 8 style guide
- Write tests for new features
- Document API changes
- Handle errors gracefully
- Use appropriate language detection
- Maintain consistent response formats

### Environment Variables
- `API_KEY` - IBM Watson API key
- `PROJECT_ID` - IBM Watson project ID
- `BASE_URL` - (Optional) Custom API base URL

## Environment Setup

1. Create a `.env` file in the `backend` directory:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. Update the `.env` file with your IBM Watson credentials:
   ```bash
   API_KEY=your_ibm_api_key
   IAM_APIKEY=your_ibm_api_key
   BASE_URL=https://api.dataplatform.cloud.ibm.com/v2/wca/core/chat/text/generation
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

# Code Explanation API

A FastAPI-based service that provides code explanation in multiple languages using WatsonX.ai.

## Features

- Code explanation in multiple languages:
  - Traditional Chinese
  - Simplified Chinese
  - Korean
  - Thai
  - Indonesian
  - Vietnamese
  - English (default)
- Error handling with graceful fallbacks
- Language detection from user messages
- Support for various programming languages

## API Endpoints

### POST /chat
Process chat messages and return code explanations in the detected language.

Request:
```json
{
  "message": "Please explain this code",
  "code": "def example(): return 'Hello World'",
  "history": []
}
```

Response:
```json
{
  "answer": "Explanation in requested language",
  "context": []
}
```

### POST /explain/{language}
Explain code in a specific language (e.g., /explain/traditional_chinese)

Request:
```json
{
  "code": "def example(): return 'Hello World'"
}
```

Response:
```json
{
  "explanation": "Code explanation in requested language",
  "analysis": []
}
```

## Setup

1. Create a `.env` file with:
```
API_KEY=your_watsonx_api_key
PROJECT_ID=your_watsonx_project_id
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn wca_i18n:app --reload
```

## Testing

Run tests with:
```bash
pytest
```

## Error Handling

The API provides graceful error handling:
- Empty code validation
- API key validation
- WatsonX.ai API error handling
- Language support validation

## Notes

- The service uses WatsonX.ai for code explanation
- Default language is English if no language is detected
- All responses include explanation in the requested language