import logging
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from models import db, Booking, ConversationLog

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
booking_bp = Blueprint('booking', __name__, url_prefix='/api/booking')

# Import data at function level to avoid circular imports
def get_bbq_outlets_info():
    from data.bbq_knowledge_base import bbq_outlets_info
    return bbq_outlets_info


@booking_bp.route('/create', methods=['POST'])
def create_booking():
    """Create a new booking"""
    data = request.json
    
    # Validate required fields
    required_fields = ['outlet_id', 'date', 'time', 'guests', 'customer_name', 'phone']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    try:
        # Generate unique booking ID
        booking_id = f"BBQ-{str(uuid.uuid4())[:8].upper()}"
        
        # Parse date and time
        try:
            booking_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            booking_time = datetime.strptime(data['time'], '%H:%M').time()
        except ValueError as e:
            return jsonify({
                'status': 'error',
                'message': f'Invalid date or time format: {str(e)}'
            }), 400
        
        # Create booking in database
        new_booking = Booking(
            booking_id=booking_id,
            outlet_id=data['outlet_id'],
            booking_date=booking_date,
            booking_time=booking_time,
            guests=int(data['guests']),
            customer_name=data['customer_name'],
            phone=data['phone'],
            status='confirmed'
        )
        
        db.session.add(new_booking)
        db.session.commit()
        
        # Get outlet name from ID
        outlet_name = "Barbeque Nation"
        outlets = get_bbq_outlets_info()
        for outlet in outlets:
            if outlet.get('id') == data['outlet_id']:
                outlet_name = outlet.get('name')
                break
        
        # Return success response
        return jsonify({
            'status': 'success',
            'data': {
                'booking_id': booking_id,
                'outlet': outlet_name,
                'date': data['date'],
                'time': data['time'],
                'guests': data['guests'],
                'customer_name': data['customer_name'],
                'phone': data['phone'],
                'status': 'confirmed'
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to create booking: {str(e)}'
        }), 500


@booking_bp.route('/update', methods=['PUT'])
def update_booking():
    """Update an existing booking"""
    data = request.json
    
    # Validate booking ID
    booking_id = data.get('booking_id')
    if not booking_id:
        return jsonify({
            'status': 'error',
            'message': 'Booking ID is required'
        }), 400
    
    try:
        # Find booking in database
        booking = Booking.query.filter_by(booking_id=booking_id).first()
        if not booking:
            return jsonify({
                'status': 'error',
                'message': f'Booking not found with ID: {booking_id}'
            }), 404
        
        # Update booking fields
        updated_fields = []
        
        if 'outlet_id' in data and data['outlet_id']:
            booking.outlet_id = data['outlet_id']
            updated_fields.append('outlet')
        
        if 'date' in data and data['date']:
            try:
                booking.booking_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
                updated_fields.append('date')
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid date format. Use YYYY-MM-DD.'
                }), 400
        
        if 'time' in data and data['time']:
            try:
                booking.booking_time = datetime.strptime(data['time'], '%H:%M').time()
                updated_fields.append('time')
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid time format. Use HH:MM.'
                }), 400
        
        if 'guests' in data and data['guests']:
            booking.guests = int(data['guests'])
            updated_fields.append('guest count')
        
        if 'status' in data and data['status']:
            booking.status = data['status']
            updated_fields.append('status')
        
        # Update timestamp
        booking.updated_at = datetime.utcnow()
        
        # Save changes
        db.session.commit()
        
        # Return success response
        return jsonify({
            'status': 'success',
            'data': {
                'booking_id': booking.booking_id,
                'message': 'Booking updated successfully',
                'updated_fields': ', '.join(updated_fields),
                'booking': booking.to_dict()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating booking: {str(e)}")
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to update booking: {str(e)}'
        }), 500


@booking_bp.route('/cancel', methods=['POST'])
def cancel_booking():
    """Cancel a booking"""
    data = request.json
    
    # Validate booking ID or phone
    booking_id = data.get('booking_id')
    phone = data.get('phone')
    
    if not booking_id and not phone:
        return jsonify({
            'status': 'error',
            'message': 'Either booking ID or phone number is required'
        }), 400
    
    try:
        # Find booking in database
        if booking_id:
            booking = Booking.query.filter_by(booking_id=booking_id).first()
        else:
            booking = Booking.query.filter_by(phone=phone).order_by(Booking.created_at.desc()).first()
        
        if not booking:
            return jsonify({
                'status': 'error',
                'message': 'Booking not found with the provided information'
            }), 404
        
        # Update booking status
        booking.status = 'cancelled'
        booking.updated_at = datetime.utcnow()
        
        # Save changes
        db.session.commit()
        
        # Return success response
        return jsonify({
            'status': 'success',
            'data': {
                'booking_id': booking.booking_id,
                'message': 'Booking cancelled successfully',
                'status': 'cancelled'
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error cancelling booking: {str(e)}")
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to cancel booking: {str(e)}'
        }), 500


@booking_bp.route('/find', methods=['GET'])
def find_booking():
    """Find a booking by ID or phone number"""
    booking_id = request.args.get('booking_id')
    phone = request.args.get('phone')
    
    if not booking_id and not phone:
        return jsonify({
            'status': 'error',
            'message': 'Either booking ID or phone number is required'
        }), 400
    
    try:
        # Find booking in database
        if booking_id:
            booking = Booking.query.filter_by(booking_id=booking_id).first()
        else:
            booking = Booking.query.filter_by(phone=phone).order_by(Booking.created_at.desc()).first()
        
        if not booking:
            return jsonify({
                'status': 'error',
                'message': 'Booking not found with the provided information'
            }), 404
        
        # Get outlet name
        outlet_name = "Barbeque Nation"
        outlets = get_bbq_outlets_info()
        for outlet in outlets:
            if outlet.get('id') == booking.outlet_id:
                outlet_name = outlet.get('name')
                break
        
        # Convert booking to dict and add outlet name
        booking_dict = booking.to_dict()
        booking_dict['outlet_name'] = outlet_name
        
        # Return booking details
        return jsonify({
            'status': 'success',
            'data': booking_dict
        }), 200
        
    except Exception as e:
        logger.error(f"Error finding booking: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to find booking: {str(e)}'
        }), 500