# FastAPI Voice Assistant

This project is a FastAPI-based AI voice assistant that provides chat assistance, speech-to-text conversion, and text-to-speech capabilities. 

## Features

- **Chat Assistance**: Interact with the AI through text-based chat.
- **Speech to Text**: Convert spoken language into written text.
- **Text to Speech**: Generate spoken language from written text.

## Project Structure

```
fastapi-voice-assistant
├── app
│   ├── api
│   │   ├── endpoints
│   │   │   ├── chat.py
│   │   │   ├── speech_to_text.py
│   │   │   └── text_to_speech.py
│   ├── core
│   │   ├── config.py
│   │   └── settings.py
│   ├── models
│   │   └── chat.py
│   ├── services
│   │   ├── ai_service.py
│   │   ├── speech_recognition.py
│   │   ├── text_to_speech.py
│   │   └── chat_service.py
│   └── utils
│       └── audio_processing.py
├── tests
│   ├── test_chat.py
│   ├── test_speech_to_text.py
│   └── test_text_to_speech.py
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fastapi-voice-assistant.git
   cd fastapi-voice-assistant
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the FastAPI application, execute the following command:
```
uvicorn app.main:app --reload
```

You can access the API documentation at `http://127.0.0.1:8000/docs`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.