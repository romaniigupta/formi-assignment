import os
import json
import logging
import datetime
import pytz
from flask import Blueprint, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils.helpers import (
    format_date, 
    format_time, 
    get_current_ist_time, 
    format_ist_time,
    validate_phone_number,
    classify_call_outcome,
    generate_call_summary
)

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
post_call_bp = Blueprint('post_call', __name__)

# Initialize Google Sheets connection
def get_sheets_client():
    """Initialize and return Google Sheets client"""
    try:
        # First check for credentials file path
        creds_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if creds_file and os.path.exists(creds_file):
            # OAuth2 credentials from file
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
            return gspread.authorize(credentials)
        
        # Next try to use service account credentials from environment variable
        creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        if creds_json:
            # Parse JSON from environment variable
            import json
            creds_dict = json.loads(creds_json)
            
            # OAuth2 credentials from dict
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            
            return gspread.authorize(credentials)
        else:
            logger.warning("Google credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_CREDENTIALS_JSON environment variables to enable Google Sheets logging.")
            return None
    except Exception as e:
        logger.error(f"Error initializing Google Sheets client: {str(e)}")
        return None

@post_call_bp.route('/log', methods=['POST'])
def log_conversation():
    """Log conversation data to Google Sheets"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['modality', 'phone_number', 'conversation']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
            
        # Extract and validate data
        modality = data.get('modality', 'Chatbot')
        phone_number = validate_phone_number(data.get('phone_number', ''))
        conversation = data.get('conversation', '')
        
        # Validate phone number format
        if not phone_number:
            return jsonify({
                "status": "error",
                "message": "Invalid phone number format"
            }), 400
            
        # Get current time in IST
        call_time = format_ist_time()
        
        # Extract or use provided values
        call_outcome = data.get('call_outcome') or classify_call_outcome(conversation)
        outlet_name = data.get('outlet_name', 'NA')
        booking_date = format_date(data.get('booking_date', 'NA'))
        booking_time = format_time(data.get('booking_time', 'NA'))
        customer_name = data.get('customer_name', 'NA')
        guests = data.get('guests', 'NA')
        call_summary = data.get('call_summary') or generate_call_summary(conversation)
        
        # Create row data for Google Sheets
        row_data = [
            modality,
            call_time,
            phone_number,
            call_outcome,
            outlet_name,
            booking_date,
            booking_time,
            guests,
            call_summary,
            conversation[:1000]  # Truncated conversation text to avoid exceeding sheet limits
        ]
        
        # Also save to database
        try:
            from models import db, ConversationLog
            
            # Create new conversation log entry
            new_log = ConversationLog(
                modality=modality,
                phone_number=phone_number,
                call_outcome=call_outcome,
                outlet_name=outlet_name,
                booking_date=booking_date,
                booking_time=booking_time,
                guests=str(guests),
                call_summary=call_summary,
                conversation_text=conversation
            )
            
            # Save to database
            db.session.add(new_log)
            db.session.commit()
            logger.info(f"Conversation log saved to database with ID: {new_log.id}")
        except Exception as db_error:
            logger.error(f"Error saving to database: {str(db_error)}")
            # Continue with Google Sheets logging attempt even if DB fails
        
        # Try to log data to Google Sheets
        sheets_client = get_sheets_client()
        
        if sheets_client:
            # Open the sheet using the ID from config
            sheet_id = os.environ.get('GOOGLE_SHEETS_ID')
            
            if not sheet_id:
                logger.error("Google Sheets ID not found in environment variables")
                # Fall back to local logging
                log_locally(row_data)
                
                return jsonify({
                    "status": "warning",
                    "message": "Conversation logged locally due to missing Google Sheets ID",
                    "data": row_data
                })
                
            try:
                sheet = sheets_client.open_by_key(sheet_id)
                worksheet = sheet.sheet1  # Use the first sheet
                
                # Append the row
                worksheet.append_row(row_data)
                
                return jsonify({
                    "status": "success",
                    "message": "Conversation logged successfully to Google Sheets",
                    "data": row_data
                })
            except Exception as e:
                logger.error(f"Error writing to Google Sheets: {str(e)}")
                # Fall back to local logging
                log_locally(row_data)
                
                return jsonify({
                    "status": "warning",
                    "message": f"Conversation logged locally due to Google Sheets error: {str(e)}",
                    "data": row_data
                })
        else:
            # Fall back to local logging
            log_locally(row_data)
            
            return jsonify({
                "status": "warning",
                "message": "Conversation logged locally due to Google Sheets connection failure",
                "data": row_data
            })
            
    except Exception as e:
        logger.error(f"Error logging conversation: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to log conversation",
            "error": str(e)
        }), 500

def log_locally(row_data):
    """Log data locally as a fallback"""
    try:
        # Create a unique filename based on timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"conversation_log_{timestamp}.json"
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Map row data to named fields
        log_data = {
            "modality": row_data[0],
            "call_time": row_data[1],
            "phone_number": row_data[2],
            "call_outcome": row_data[3],
            "outlet_name": row_data[4],
            "booking_date": row_data[5],
            "booking_time": row_data[6],
            "guests": row_data[7],
            "call_summary": row_data[8],
            "conversation_text": row_data[9] if len(row_data) > 9 else "N/A"
        }
        
        # Write to file
        with open(f"logs/{filename}", 'w') as f:
            json.dump(log_data, f, indent=2)
            
        logger.info(f"Conversation log saved locally to logs/{filename}")
        
    except Exception as e:
        logger.error(f"Error logging locally: {str(e)}")

@post_call_bp.route('/analyze', methods=['POST'])
def analyze_conversation():
    """
    Analyze a conversation and extract key information
    This would typically use an advanced AI model, but 
    we're implementing a simpler version here
    """
    try:
        data = request.json
        conversation = data.get('conversation', '')
        
        if not conversation:
            return jsonify({
                "status": "error",
                "message": "Conversation text is required for analysis"
            }), 400
            
        # Analyze conversation to extract key information
        call_outcome = classify_call_outcome(conversation)
        
        # Extract entities using helper function
        entities = {
            'phone': None,
            'date': 'NA',
            'time': 'NA',
            'guests': 'NA',
            'name': 'NA'
        }
        
        # Extract each entity type
        for entity_type in entities.keys():
            extracted = {}
            if entity_type == 'phone':
                # Look for phone numbers
                import re
                phone_matches = re.findall(r'(?:\+91|0)?[6-9][0-9]{9}', conversation)
                if phone_matches:
                    entities['phone'] = validate_phone_number(phone_matches[0])
            else:
                # Use helper function for other entity types
                extracted = utils.helpers.extract_entities_from_text(
                    conversation, [entity_type]
                )
                if entity_type in extracted:
                    entities[entity_type] = extracted[entity_type]
        
        # Generate summary
        call_summary = generate_call_summary(conversation)
        
        # Return the analysis
        return jsonify({
            "status": "success",
            "message": "Conversation analyzed successfully",
            "analysis": {
                "call_outcome": call_outcome,
                "booking_date": entities['date'],
                "booking_time": entities['time'],
                "customer_name": entities['name'],
                "guests": entities['guests'],
                "phone_number": entities['phone'],
                "call_summary": call_summary
            }
        })
        
    except Exception as e:
        logger.error(f"Error analyzing conversation: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to analyze conversation",
            "error": str(e)
        }), 500
