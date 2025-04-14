# SayYes Agent API

A Flask-based API for the SayYes Agent chat functionality.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file:
```bash
cp .env.example .env
```
Then edit the .env file with your specific configuration.

## Running the Application

To run the application:

```bash
python app.py
```

The server will start on port 8080 by default (or the port specified in your .env file).

## API Endpoints

- `GET /`: Root endpoint, returns API status
- `GET /api/health`: Health check endpoint
- `POST /api/chat`: Chat endpoint for processing messages

## Environment Variables

- `PORT`: The port number for the server (default: 8080) 