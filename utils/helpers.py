import re
import json
import datetime
import logging
import pytz

logger = logging.getLogger(__name__)

def format_date(date_str):
    """
    Format a date string to YYYY-MM-DD format.
    
    Args:
        date_str (str): Date string in various formats
        
    Returns:
        str: Formatted date or 'NA' if invalid
    """
    if not date_str or date_str.lower() == 'na':
        return 'NA'
        
    try:
        # Try to parse date from different formats
        for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d', '%d %B %Y', '%B %d, %Y']:
            try:
                date_obj = datetime.datetime.strptime(date_str, fmt)
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                continue
                
        # If none of the formats match, try more flexible parsing
        match = re.search(r'(\d{1,2})[-/\s]?(\d{1,2}|[A-Za-z]+)[-/\s]?(\d{2,4})', date_str)
        if match:
            day, month, year = match.groups()
            
            # Handle month names
            if month.isalpha():
                month = datetime.datetime.strptime(month, '%B').month
                
            # Handle two-digit years
            if len(year) == 2:
                year = '20' + year if int(year) < 50 else '19' + year
                
            date_obj = datetime.datetime(int(year), int(month), int(day))
            return date_obj.strftime('%Y-%m-%d')
            
        return 'NA'
    except Exception as e:
        logger.error(f"Error formatting date {date_str}: {str(e)}")
        return 'NA'

def format_time(time_str):
    """
    Format a time string to HH:MM format.
    
    Args:
        time_str (str): Time string in various formats
        
    Returns:
        str: Formatted time or 'NA' if invalid
    """
    if not time_str or time_str.lower() == 'na':
        return 'NA'
        
    try:
        # Try to parse time from different formats
        for fmt in ['%H:%M', '%I:%M %p', '%H:%M:%S', '%I:%M:%S %p']:
            try:
                time_obj = datetime.datetime.strptime(time_str, fmt)
                return time_obj.strftime('%H:%M')
            except ValueError:
                continue
                
        # Try more flexible parsing
        match = re.search(r'(\d{1,2})[:\.]?(\d{2})(?:\s*(am|pm|AM|PM))?', time_str)
        if match:
            hour, minute, period = match.groups() if len(match.groups()) == 3 else (*match.groups(), None)
            
            # Convert 12-hour to 24-hour format if period is specified
            if period and period.lower() == 'pm' and int(hour) < 12:
                hour = str(int(hour) + 12)
            if period and period.lower() == 'am' and int(hour) == 12:
                hour = '0'
                
            # Pad hour with zeros if needed
            if len(hour) == 1:
                hour = '0' + hour
                
            return f"{hour}:{minute}"
            
        return 'NA'
    except Exception as e:
        logger.error(f"Error formatting time {time_str}: {str(e)}")
        return 'NA'

def get_current_ist_time():
    """
    Get current time in Indian Standard Time.
    
    Returns:
        datetime: Current datetime in IST
    """
    ist_timezone = pytz.timezone('Asia/Kolkata')
    return datetime.datetime.now(ist_timezone)

def format_ist_time(dt=None):
    """
    Format datetime in IST format.
    
    Args:
        dt (datetime, optional): Datetime to format. Defaults to current time.
        
    Returns:
        str: Formatted datetime string
    """
    if dt is None:
        dt = get_current_ist_time()
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def validate_phone_number(phone):
    """
    Validate Indian phone number format.
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        str: Cleaned phone number or None if invalid
    """
    if not phone:
        return None
        
    # Remove all non-digit characters
    cleaned = re.sub(r'\D', '', phone)
    
    # Check if it's a valid indian number (10 digits, optionally with country code)
    if len(cleaned) == 10 and cleaned[0] in '6789':
        return cleaned
    elif len(cleaned) > 10 and cleaned.endswith(('6', '7', '8', '9')):
        # Extract the last 10 digits
        return cleaned[-10:]
    return None

def extract_entities_from_text(text, entity_types):
    """
    Extract entities from text using simple regex patterns.
    
    Args:
        text (str): Text to extract entities from
        entity_types (list): List of entity types to extract
        
    Returns:
        dict: Extracted entities
    """
    entities = {}
    
    if 'phone' in entity_types:
        # Match phone numbers (with or without country code)
        phone_matches = re.findall(r'(?:\+91|0)?[6-9][0-9]{9}', text)
        if phone_matches:
            entities['phone'] = validate_phone_number(phone_matches[0])
    
    if 'date' in entity_types:
        # Match date patterns
        date_matches = re.findall(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}-\d{2}-\d{2}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}', text, re.IGNORECASE)
        if date_matches:
            entities['date'] = format_date(date_matches[0])
    
    if 'time' in entity_types:
        # Match time patterns
        time_matches = re.findall(r'\d{1,2}:\d{2}(?::\d{2})?\s*(?:am|pm)?|\d{1,2}\s*(?:am|pm)', text, re.IGNORECASE)
        if time_matches:
            entities['time'] = format_time(time_matches[0])
    
    if 'guests' in entity_types:
        # Match number of guests
        guest_matches = re.findall(r'(\d+)\s+(?:guest|people|person|adult|customer)', text, re.IGNORECASE)
        if guest_matches:
            entities['guests'] = int(guest_matches[0])
    
    if 'name' in entity_types:
        # This is more complex, might need more sophisticated NLP
        # For now, look for common name patterns
        name_matches = re.findall(r'(?:my name is|this is|I am|I\'m)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})', text)
        if name_matches:
            entities['name'] = name_matches[0]
    
    return entities

def classify_call_outcome(conversation):
    """
    Classify the outcome of a call based on conversation text.
    
    Args:
        conversation (str): Full conversation text
        
    Returns:
        str: Classified outcome
    """
    # Simple keyword-based classification
    if re.search(r'book|reserve|table|reservation', conversation, re.IGNORECASE):
        if re.search(r'modify|change|update|cancel|reschedule', conversation, re.IGNORECASE):
            return "Post-Booking"
        return "Availability"
    elif re.search(r'question|faq|ask|tell me|how|what|when|where|why', conversation, re.IGNORECASE):
        return "Enquiry"
    else:
        return "Misc"

def generate_call_summary(conversation):
    """
    Generate a summary of the call using simple text analysis.
    This would ideally use an AI model, but we're using a simple approach here.
    
    Args:
        conversation (str): Full conversation text
        
    Returns:
        str: Generated summary
    """
    # Extract key information to include in summary
    outcome = classify_call_outcome(conversation)
    entities = extract_entities_from_text(conversation, ['date', 'time', 'guests', 'name', 'phone'])
    
    # Create summary based on outcome type
    if outcome == "Availability":
        date_str = entities.get('date', 'NA')
        time_str = entities.get('time', 'NA')
        guests = entities.get('guests', 'NA')
        name = entities.get('name', 'the customer')
        
        return f"{name} enquired about booking a table " + \
               (f"for {guests} guests " if guests != 'NA' else "") + \
               (f"on {date_str} " if date_str != 'NA' else "") + \
               (f"at {time_str}. " if time_str != 'NA' else ". ") + \
               "The customer was informed about availability and booking process."
    
    elif outcome == "Post-Booking":
        return f"The customer contacted regarding an existing booking. " + \
               "They were assisted with modifications or cancellation requests for their reservation."
    
    elif outcome == "Enquiry":
        return "The customer had general enquiries about Barbeque Nation. " + \
               "Information was provided regarding menu, pricing, location, or other details."
    
    else:
        return "The customer contacted for miscellaneous reasons. " + \
               "The conversation did not result in a specific booking or enquiry resolution."
