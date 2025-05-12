import os
import json
import logging
from flask import Blueprint, request, jsonify
from utils.token_management import TokenManager
from data.bbq_knowledge_base import (
    bbq_outlets_info, 
    bbq_faq_info, 
    bbq_menu_info
)

# Configure logging
logger = logging.getLogger(__name__)

# Configure token management
token_manager = TokenManager(max_tokens=800)

# Create blueprint
knowledge_base_bp = Blueprint('knowledge_base', __name__)

@knowledge_base_bp.route('/outlets', methods=['GET'])
def get_outlets_info():
    """Get information about Barbeque Nation outlets"""
    try:
        location = request.args.get('location', '').capitalize()
        outlet_id = request.args.get('outlet_id')
        
        # Filter by location if provided
        if location:
            outlets = [outlet for outlet in bbq_outlets_info if outlet.get('city', '').lower() == location.lower()]
        else:
            outlets = bbq_outlets_info
            
        # Filter by outlet_id if provided
        if outlet_id:
            outlets = [outlet for outlet in outlets if str(outlet.get('id')) == outlet_id]
            
        if not outlets:
            return jsonify({
                "status": "error",
                "message": f"No outlets found for the specified criteria.",
                "data": []
            }), 404
            
        # Important fields to prioritize in responses
        important_fields = ["id", "name", "address", "city", "phone", "opening_hours"]
        
        # Optimize the response to stay under token limit
        optimized_outlets = token_manager.optimize_response(outlets, important_fields)
        
        return jsonify({
            "status": "success",
            "message": f"Found {len(optimized_outlets)} outlets",
            "data": optimized_outlets
        })
        
    except Exception as e:
        logger.error(f"Error retrieving outlet information: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve outlet information",
            "error": str(e)
        }), 500

@knowledge_base_bp.route('/faq', methods=['GET'])
def get_faq_info():
    """Get FAQ information for Barbeque Nation"""
    try:
        query = request.args.get('query', '').lower()
        category = request.args.get('category')
        
        # Filter by category if provided
        if category:
            faqs = [faq for faq in bbq_faq_info if faq.get('category', '').lower() == category.lower()]
        else:
            faqs = bbq_faq_info
            
        # Filter by query if provided
        if query:
            filtered_faqs = []
            for faq in faqs:
                # Check if query is in question or answer
                if (query in faq.get('question', '').lower() or 
                    query in faq.get('answer', '').lower()):
                    filtered_faqs.append(faq)
            faqs = filtered_faqs
            
        if not faqs:
            return jsonify({
                "status": "error",
                "message": "No FAQ matches found for the specified criteria.",
                "data": []
            }), 404
            
        # Important fields to prioritize in responses
        important_fields = ["question", "answer", "category"]
        
        # Optimize the response to stay under token limit
        optimized_faqs = token_manager.optimize_response(faqs, important_fields)
        
        return jsonify({
            "status": "success",
            "message": f"Found {len(optimized_faqs)} FAQs",
            "data": optimized_faqs
        })
        
    except Exception as e:
        logger.error(f"Error retrieving FAQ information: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve FAQ information",
            "error": str(e)
        }), 500

@knowledge_base_bp.route('/menu', methods=['GET'])
def get_menu_info():
    """Get menu information for Barbeque Nation"""
    try:
        category = request.args.get('category')
        item_name = request.args.get('item_name', '').lower()
        
        # Filter by category if provided
        if category:
            menu_items = [item for item in bbq_menu_info if item.get('category', '').lower() == category.lower()]
        else:
            menu_items = bbq_menu_info
            
        # Filter by item name if provided
        if item_name:
            menu_items = [item for item in menu_items if item_name in item.get('name', '').lower()]
            
        if not menu_items:
            return jsonify({
                "status": "error",
                "message": "No menu items found for the specified criteria.",
                "data": []
            }), 404
            
        # Important fields to prioritize in responses
        important_fields = ["name", "description", "price", "category", "is_vegetarian"]
        
        # Optimize the response to stay under token limit
        optimized_menu = token_manager.optimize_response(menu_items, important_fields)
        
        return jsonify({
            "status": "success",
            "message": f"Found {len(optimized_menu)} menu items",
            "data": optimized_menu
        })
        
    except Exception as e:
        logger.error(f"Error retrieving menu information: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve menu information",
            "error": str(e)
        }), 500

@knowledge_base_bp.route('/bookings', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_bookings():
    """Manage booking information for Barbeque Nation"""
    try:
        # This would interface with a real booking system in production
        # For now, we'll return synthesized responses based on the query
        
        if request.method == 'GET':
            # Get booking information
            booking_id = request.args.get('booking_id')
            phone = request.args.get('phone')
            
            if booking_id:
                # Sample response for an existing booking
                booking_data = {
                    "id": booking_id,
                    "status": "confirmed",
                    "outlet": "Barbeque Nation - Koramangala",
                    "date": "2023-12-15",
                    "time": "19:30",
                    "guests": 4,
                    "customer_name": "Test User",
                    "phone": phone or "9876543210"
                }
                
                return jsonify({
                    "status": "success",
                    "message": f"Booking found",
                    "data": booking_data
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "Booking ID is required to fetch booking details",
                }), 400
                
        elif request.method == 'POST':
            # Create new booking
            data = request.json
            required_fields = ['outlet_id', 'date', 'time', 'guests', 'customer_name', 'phone']
            
            # Validate input
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required fields: {', '.join(missing_fields)}",
                }), 400
                
            # In a real implementation, this would create a booking in the database
            # For now, return a sample successful response
            booking_id = "BBQ" + data.get('phone', '')[-4:] + "123"
            
            return jsonify({
                "status": "success",
                "message": "Booking created successfully",
                "data": {
                    "booking_id": booking_id,
                    "outlet": data.get('outlet_id'),
                    "date": data.get('date'),
                    "time": data.get('time'),
                    "guests": data.get('guests'),
                    "customer_name": data.get('customer_name'),
                    "phone": data.get('phone'),
                    "status": "confirmed"
                }
            }), 201
            
        elif request.method == 'PUT':
            # Update existing booking
            data = request.json
            booking_id = data.get('booking_id')
            
            if not booking_id:
                return jsonify({
                    "status": "error",
                    "message": "Booking ID is required to update a booking",
                }), 400
                
            # In a real implementation, this would update the booking in the database
            # For now, return a sample successful response
            return jsonify({
                "status": "success",
                "message": "Booking updated successfully",
                "data": {
                    "booking_id": booking_id,
                    "outlet": data.get('outlet_id', "Barbeque Nation - Koramangala"),
                    "date": data.get('date', "2023-12-15"),
                    "time": data.get('time', "19:30"),
                    "guests": data.get('guests', 4),
                    "customer_name": data.get('customer_name', "Test User"),
                    "phone": data.get('phone', "9876543210"),
                    "status": "updated"
                }
            })
            
        elif request.method == 'DELETE':
            # Cancel booking
            booking_id = request.args.get('booking_id')
            
            if not booking_id:
                return jsonify({
                    "status": "error",
                    "message": "Booking ID is required to cancel a booking",
                }), 400
                
            # In a real implementation, this would cancel the booking in the database
            # For now, return a sample successful response
            return jsonify({
                "status": "success",
                "message": "Booking cancelled successfully",
                "data": {
                    "booking_id": booking_id,
                    "status": "cancelled"
                }
            })
            
    except Exception as e:
        logger.error(f"Error managing booking: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to process booking request",
            "error": str(e)
        }), 500

@knowledge_base_bp.route('/outlets', methods=['GET'])
def get_outlets():
    """Get all outlets information"""
    try:
        return jsonify({
            "status": "success",
            "data": bbq_outlets_info
        })
    except Exception as e:
        logger.error(f"Error getting outlets: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve outlets information"
        }), 500

@knowledge_base_bp.route('/query', methods=['POST'])
def query_knowledge_base():
    """General endpoint to query the knowledge base"""
    try:
        data = request.json
        query_text = data.get('query', '')
        query_type = data.get('type', 'general')
        
        if not query_text:
            return jsonify({
                "status": "error",
                "message": "Query text is required",
            }), 400
            
        query_text = query_text.lower()
        
        # Determine the relevant knowledge base to query
        if any(keyword in query_text for keyword in ['location', 'outlet', 'address', 'branch', 'where']):
            # Query about outlet locations
            response = {"type": "outlets", "data": []}
            for outlet in bbq_outlets_info:
                city = outlet.get('city', '').lower()
                if city in query_text:
                    response["data"].append(outlet)
            
            if not response["data"]:
                # If no specific city found, return outlets for both Delhi and Bangalore
                response["data"] = bbq_outlets_info
                
        elif any(keyword in query_text for keyword in ['menu', 'food', 'dish', 'item', 'price', 'cost']):
            # Query about menu
            response = {"type": "menu", "data": []}
            
            # Check for specific categories
            categories = ['starters', 'main course', 'desserts', 'beverages']
            found_categories = [c for c in categories if c in query_text]
            
            if found_categories:
                for item in bbq_menu_info:
                    if item.get('category', '').lower() in found_categories:
                        response["data"].append(item)
            else:
                # If no specific category, return items that match query terms
                for item in bbq_menu_info:
                    item_name = item.get('name', '').lower()
                    item_desc = item.get('description', '').lower()
                    if any(term in item_name or term in item_desc for term in query_text.split()):
                        response["data"].append(item)
                        
            if not response["data"]:
                # If no specific items found, return a sample of menu items
                response["data"] = bbq_menu_info[:5]
                
        elif any(keyword in query_text for keyword in ['book', 'reservation', 'table', 'reserve']):
            # Query about booking
            response = {
                "type": "booking",
                "message": "To make a reservation at Barbeque Nation, I'll need the following details: date, time, number of guests, your name, and contact number. Would you like to proceed with a booking?"
            }
            
        else:
            # General FAQ query
            response = {"type": "faq", "data": []}
            
            # Find FAQs that match the query
            for faq in bbq_faq_info:
                question = faq.get('question', '').lower()
                answer = faq.get('answer', '').lower()
                
                # Calculate a simple relevance score
                # Count how many words in the query match words in question or answer
                query_words = set(query_text.split())
                question_words = set(question.split())
                answer_words = set(answer.split())
                
                score = len(query_words.intersection(question_words)) * 2 + len(query_words.intersection(answer_words))
                
                if score > 0:
                    faq['relevance_score'] = score
                    response["data"].append(faq)
                    
            # Sort by relevance score
            response["data"] = sorted(response["data"], key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            if not response["data"]:
                # If no FAQs found, return a default message
                response = {
                    "type": "general",
                    "message": "I'm here to help you with information about Barbeque Nation, including our outlets in Delhi and Bangalore, menu options, and booking assistance. Please let me know what you'd like to know."
                }
        
        # Ensure the response fits within token limits
        optimized_response = token_manager.optimize_response(response)
        
        return jsonify({
            "status": "success",
            "message": "Knowledge base query processed successfully",
            "result": optimized_response
        })
        
    except Exception as e:
        logger.error(f"Error processing knowledge base query: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to process knowledge base query",
            "error": str(e)
        }), 500
