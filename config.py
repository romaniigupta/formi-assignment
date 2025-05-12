import os

class Config:
    """Application configuration settings"""
    
    # App config
    DEBUG = True
    TESTING = False
    
    # Google Sheets credentials and config
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_SHEETS_ID = os.environ.get('GOOGLE_SHEETS_ID')
    
    # RetellAI configuration
    RETELL_API_KEY = os.environ.get('RETELL_API_KEY')
    RETELL_ENDPOINT = "https://api.retellai.com/v1"
    
    # Knowledge base configuration
    MAX_TOKEN_SIZE = 800  # Maximum token size for knowledge base responses
    
    # Location specific data
    LOCATIONS = ["Delhi", "Bangalore"]
    
    # Call outcome types
    CALL_OUTCOMES = [
        "Enquiry", 
        "Availability", 
        "Post-Booking", 
        "Misc"
    ]
