# Barbeque Nation Conversational AI System

A state machine-based conversational AI system for Barbeque Nation that handles enquiries, bookings, and booking modifications for outlets in Delhi and Bangalore.

## Project Description

This project implements a conversational AI system for Barbeque Nation, enabling:

- Answering FAQs about outlets, menu, pricing, etc.
- Creating new table bookings
- Modifying or cancelling existing bookings
- Post-call analysis with logging to Google Sheets

The system uses a state machine architecture to manage conversation flow, with defined state prompts and transition rules. It integrates with RetellAI for advanced language processing.

## Features

- **Knowledge Base**: Structured data for Delhi and Bangalore outlets, including location, menu, and FAQ information
- **Booking System**: Create, modify, and cancel reservations through chat or direct forms
- **Post-Call Analysis**: Log and analyze conversation data in Google Sheets
- **Chatbot Interface**: Web-based interface for interacting with the AI system

## System Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌───────────────────┐
│   User Interface│     │  State Machine   │     │   Knowledge Base  │
│  (Chat/Forms)   │────▶│ (RetellAI Based) │────▶│  (Delhi/Bangalore)│
└─────────────────┘     └──────────────────┘     └───────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌──────────────────┐     ┌───────────────────┐
│  Booking System │     │ Logging System   │     │     Database      │
│ (Create/Modify/ │◀───▶│ (Google Sheets)  │◀───▶│(PostgreSQL)       │
│    Cancel)      │     │                  │     │                   │
└─────────────────┘     └──────────────────┘     └───────────────────┘
```

## API Documentation

### Knowledge Base Endpoints

- `GET /api/knowledge/outlets` - Get all BBQ Nation outlets
- `GET /api/knowledge/outlets?city=Delhi` - Get outlets filtered by city
- `POST /api/knowledge/query` - Query the knowledge base with natural language

### Booking Endpoints

- `POST /api/booking/create` - Create a new booking
- `PUT /api/booking/update` - Update an existing booking
- `POST /api/booking/cancel` - Cancel a booking
- `GET /api/booking/find` - Find a booking by ID or phone

### Conversation & Analysis Endpoints

- `POST /api/conversation/function_call` - Make a function call to the conversation service
- `POST /api/logs/log` - Log conversation data to Google Sheets

## Required Links (Submission)

- **Knowledge Base API Endpoints**: 
  - Base URL: `https://bbq-conversation-ai.example.com/api/knowledge`
  - Documentation: See API Documentation section

- **Post-Call Analysis Sheet**:
  - Google Sheets Link: [BBQ Nation Conversation Logs](https://docs.google.com/spreadsheets/d/your-sheet-id)

- **Chatbot Link**:
  - Web Interface: `https://bbq-conversation-ai.example.com/chat`
  - Direct Form: `https://bbq-conversation-ai.example.com/booking`

- **Agent Phone Number**:
  - RetellAI Demo Number: +1-XXX-XXX-XXXX

## Technical Implementation Details

### State Machine

The conversation flow follows a state machine architecture with the following main states:
- Greeting
- FAQ Enquiry
- Booking Collection
- Booking Confirmation
- Booking Modification
- Booking Cancellation

Each state has a specific prompt and transition rules defined in `api/state_machine.py`.

### Knowledge Base

The knowledge base is structured as JSON data containing:
- Outlet information (location, timings, features)
- Menu details (with veg/non-veg indicators)
- FAQ information organized by category

The data is stored in `data/bbq_knowledge_base.py` and exposed through API endpoints.

### Post-Call Analysis

Conversation data is logged to a Google Sheet with the following columns:
- Modality (Call/Chatbot)
- Call Time
- Phone Number
- Call Outcome
- Outlet
- Booking Date
- Booking Time
- Guests
- Call Summary
- Conversation Text

## Setup and Deployment

### Prerequisites

- Python 3.10+
- PostgreSQL database
- Google Cloud credentials (for Sheets API)
- RetellAI account and API keys

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `GOOGLE_CREDENTIALS_JSON`: Google service account credentials in JSON format
- `GOOGLE_SHEETS_ID`: ID of the Google Sheet for logging
- `RETELL_API_KEY`: API key for RetellAI platform
- `SESSION_SECRET`: Secret key for session management

### Installation

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables
4. Initialize the database: `flask db upgrade`
5. Run the server: `gunicorn --bind 0.0.0.0:5000 main:app`

## Integration with RetellAI

This system integrates with RetellAI for state machine handling. The integration uses the function calling capability to:
1. Manage state transitions
2. Process natural language understanding
3. Generate appropriate responses based on the current state

The RetellAI integration code is in `api/conversation_service.py`.

## License

This project is created for assessment purposes only.