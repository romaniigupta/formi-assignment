from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

class Booking(db.Model):
    """Model for restaurant bookings"""
    
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String(20), unique=True, nullable=False)
    outlet_id = db.Column(db.String(20), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(20), default='confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert booking to dictionary"""
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'outlet': self.outlet_id,
            'date': self.booking_date.strftime('%Y-%m-%d'),
            'time': self.booking_time.strftime('%H:%M'),
            'guests': self.guests,
            'customer_name': self.customer_name,
            'phone': self.phone,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class ConversationLog(db.Model):
    """Model for conversation logs"""
    
    __tablename__ = 'conversation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    modality = db.Column(db.String(20), nullable=False)  # 'Call' or 'Chatbot'
    call_time = db.Column(db.DateTime, default=datetime.utcnow)
    phone_number = db.Column(db.String(15))
    call_outcome = db.Column(db.String(50))  # 'Enquiry', 'Availability', 'Post-Booking', 'Misc'
    outlet_name = db.Column(db.String(100))
    booking_date = db.Column(db.String(10))  # YYYY-MM-DD format
    booking_time = db.Column(db.String(5))   # HH:MM format
    guests = db.Column(db.String(10))
    call_summary = db.Column(db.Text)
    conversation_text = db.Column(db.Text)
    
    def to_dict(self):
        """Convert log to dictionary"""
        return {
            'id': self.id,
            'modality': self.modality,
            'call_time': self.call_time.strftime('%Y-%m-%d %H:%M:%S'),
            'phone_number': self.phone_number,
            'call_outcome': self.call_outcome,
            'outlet_name': self.outlet_name,
            'booking_date': self.booking_date,
            'booking_time': self.booking_time,
            'guests': self.guests,
            'call_summary': self.call_summary
        }