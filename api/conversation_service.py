import os
import json
import logging
import requests
from flask import Blueprint, request, jsonify
from utils.token_management import TokenManager
from api.state_machine import StateTransition

# Configure logging
logger = logging.getLogger(__name__)

# Initialize token manager
token_manager = TokenManager(max_tokens=800)

# Create blueprint
conversation_bp = Blueprint('conversation', __name__)

# RetellAI configuration
RETELL_API_KEY = os.environ.get('RETELL_API_KEY')
RETELL_ENDPOINT = "https://api.retellai.com/v1"
HEADERS = {
    "Authorization": f"Bearer {RETELL_API_KEY}",
    "Content-Type": "application/json"
}

# State transition manager
state_transition = StateTransition()

@conversation_bp.route('/get-state-prompt', methods=['POST'])
def get_state_prompt():
    """Get the prompt for the current state"""
    try:
        data = request.json
        current_state = data.get('current_state', 'greeting')
        context = data.get('context', {})
        
        # Get the prompt for the current state
        prompt_template = state_transition.get_state_prompt(current_state)
        
        # Fill the template with context variables
        from jinja2 import Template
        template = Template(prompt_template)
        filled_prompt = template.render(**context)
        
        # Ensure the prompt fits within token limits
        truncated_prompt = token_manager.truncate_to_max_tokens(filled_prompt)
        
        return jsonify({
            "status": "success",
            "state": current_state,
            "prompt": truncated_prompt
        })
        
    except Exception as e:
        logger.error(f"Error getting state prompt: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to get state prompt",
            "error": str(e)
        }), 500

@conversation_bp.route('/transition', methods=['POST'])
def transition_state():
    """Determine the next state based on current state and user input"""
    try:
        data = request.json
        current_state = data.get('current_state', 'greeting')
        user_input = data.get('user_input', '')
        context = data.get('context', {})
        
        # Determine the next state
        next_state, updated_context = state_transition.determine_next_state(
            current_state, user_input, context
        )
        
        return jsonify({
            "status": "success",
            "previous_state": current_state,
            "next_state": next_state,
            "updated_context": updated_context
        })
        
    except Exception as e:
        logger.error(f"Error transitioning state: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to transition state",
            "error": str(e)
        }), 500

@conversation_bp.route('/retell/create-agent', methods=['POST'])
def create_retell_agent():
    """Create a new agent on RetellAI platform"""
    try:
        data = request.json
        agent_name = data.get('agent_name', 'Barbeque Nation Assistant')
        initial_state = data.get('initial_state', 'greeting')
        
        # Prepare the agent configuration
        agent_config = {
            "name": agent_name,
            "llm_model": "gpt-3.5-turbo",
            "voice_id": "alia",  # Using a standard RetellAI voice
            "initial_state": initial_state
        }
        
        # Make request to RetellAI API
        if RETELL_API_KEY:
            response = requests.post(
                f"{RETELL_ENDPOINT}/agents",
                headers=HEADERS,
                json=agent_config
            )
            
            if response.status_code == 200 or response.status_code == 201:
                agent_data = response.json()
                return jsonify({
                    "status": "success",
                    "message": "RetellAI agent created successfully",
                    "agent": agent_data
                })
            else:
                logger.error(f"Error from RetellAI: {response.text}")
                return jsonify({
                    "status": "error",
                    "message": "Failed to create RetellAI agent",
                    "error": response.text
                }), response.status_code
        else:
            # Simulate response for testing without API key
            return jsonify({
                "status": "warning",
                "message": "RetellAI API key not configured",
                "agent": {
                    "id": "test_agent_id",
                    "name": agent_name,
                    "initial_state": initial_state
                }
            })
            
    except Exception as e:
        logger.error(f"Error creating RetellAI agent: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to create RetellAI agent",
            "error": str(e)
        }), 500

@conversation_bp.route('/retell/update-agent', methods=['PUT'])
def update_retell_agent():
    """Update an existing agent on RetellAI platform"""
    try:
        data = request.json
        agent_id = data.get('agent_id')
        
        if not agent_id:
            return jsonify({
                "status": "error",
                "message": "Agent ID is required"
            }), 400
            
        # Prepare the update configuration
        update_config = {
            "name": data.get('agent_name'),
            "llm_model": data.get('llm_model'),
            "voice_id": data.get('voice_id'),
            "initial_state": data.get('initial_state')
        }
        
        # Remove None values
        update_config = {k: v for k, v in update_config.items() if v is not None}
        
        # Make request to RetellAI API
        if RETELL_API_KEY:
            response = requests.put(
                f"{RETELL_ENDPOINT}/agents/{agent_id}",
                headers=HEADERS,
                json=update_config
            )
            
            if response.status_code == 200:
                agent_data = response.json()
                return jsonify({
                    "status": "success",
                    "message": "RetellAI agent updated successfully",
                    "agent": agent_data
                })
            else:
                logger.error(f"Error from RetellAI: {response.text}")
                return jsonify({
                    "status": "error",
                    "message": "Failed to update RetellAI agent",
                    "error": response.text
                }), response.status_code
        else:
            # Simulate response for testing without API key
            return jsonify({
                "status": "warning",
                "message": "RetellAI API key not configured",
                "agent": {
                    "id": agent_id,
                    "name": update_config.get('name', 'Barbeque Nation Assistant'),
                    "initial_state": update_config.get('initial_state', 'greeting')
                }
            })
            
    except Exception as e:
        logger.error(f"Error updating RetellAI agent: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to update RetellAI agent",
            "error": str(e)
        }), 500

@conversation_bp.route('/retell/function-call', methods=['POST'])
def handle_function_call():
    """Handle function calls from RetellAI platform"""
    try:
        data = request.json
        function_name = data.get('name', '')
        arguments = data.get('arguments', {})
        
        logger.info(f"Function call received: {function_name} with arguments: {arguments}")
        
        if not function_name:
            return jsonify({
                "status": "error",
                "message": "Function name is required"
            }), 400
            
        # Handle different function calls
        if function_name == 'query_knowledge_base':
            # Query the knowledge base
            query = arguments.get('query', '')
            query_type = arguments.get('type', 'general')
            
            logger.info(f"Querying knowledge base with: {query} (type: {query_type})")
            
            try:
                # Make request to knowledge base API
                kb_response = requests.post(
                    f"{request.url_root}api/knowledge/query",
                    json={"query": query, "type": query_type},
                    timeout=10
                )
                
                logger.info(f"Knowledge base response status: {kb_response.status_code}")
                
                if kb_response.status_code == 200:
                    kb_data = kb_response.json()
                    
                    # Ensure the response fits within token limits
                    result = kb_data.get('result', {})
                    optimized_result = token_manager.optimize_response(result)
                    
                    return jsonify({
                        "status": "success",
                        "data": optimized_result
                    })
                else:
                    logger.error(f"Error from knowledge base: {kb_response.text}")
                    return jsonify({
                        "status": "success",
                        "data": {
                            "type": "error",
                            "message": "I'm unable to retrieve that information at the moment. Could you please try a different question or rephrase your query?"
                        }
                    })
            except requests.RequestException as req_error:
                logger.error(f"Request error querying knowledge base: {str(req_error)}")
                return jsonify({
                    "status": "success",
                    "data": {
                        "type": "general",
                        "message": "I can help you with information about Barbeque Nation, including our outlets in Delhi and Bangalore, menu items, and reservation services. What would you like to know?"
                    }
                })
                
        elif function_name == 'create_booking':
            # Create a new booking
            booking_data = {
                "outlet_id": arguments.get('outlet_id'),
                "date": arguments.get('date'),
                "time": arguments.get('time'),
                "guests": arguments.get('guests'),
                "customer_name": arguments.get('customer_name'),
                "phone": arguments.get('phone')
            }
            
            logger.info(f"Creating booking with data: {booking_data}")
            
            try:
                # Make request to booking API
                booking_response = requests.post(
                    f"{request.url_root}api/knowledge/bookings",
                    json=booking_data,
                    timeout=10
                )
                
                logger.info(f"Booking response status: {booking_response.status_code}")
                
                if booking_response.status_code == 201:
                    booking_result = booking_response.json()
                    
                    # Ensure the response fits within token limits
                    booking_data = booking_result.get('data', {})
                    optimized_data = token_manager.optimize_response(booking_data)
                    
                    return jsonify({
                        "status": "success",
                        "data": {
                            "type": "booking_created",
                            "booking": optimized_data
                        }
                    })
                else:
                    logger.error(f"Error creating booking: {booking_response.text}")
                    return jsonify({
                        "status": "success",
                        "data": {
                            "type": "error",
                            "message": "I'm unable to complete your booking at the moment. Please check the information provided and try again."
                        }
                    })
            except requests.RequestException as req_error:
                logger.error(f"Request error creating booking: {str(req_error)}")
                return jsonify({
                    "status": "success",
                    "data": {
                        "type": "error",
                        "message": "I encountered a problem with our booking system. Please try again later or contact us directly by phone."
                    }
                })
                
        elif function_name == 'update_booking':
            # Update existing booking
            booking_data = {
                "booking_id": arguments.get('booking_id'),
                "outlet_id": arguments.get('outlet_id'),
                "date": arguments.get('date'),
                "time": arguments.get('time'),
                "guests": arguments.get('guests')
            }
            
            # Remove None values
            booking_data = {k: v for k, v in booking_data.items() if v is not None}
            
            logger.info(f"Updating booking with data: {booking_data}")
            
            try:
                # Make request to booking API
                booking_response = requests.put(
                    f"{request.url_root}api/knowledge/bookings",
                    json=booking_data,
                    timeout=10
                )
                
                logger.info(f"Update booking response status: {booking_response.status_code}")
                
                if booking_response.status_code == 200:
                    booking_result = booking_response.json()
                    
                    # Ensure the response fits within token limits
                    booking_data = booking_result.get('data', {})
                    optimized_data = token_manager.optimize_response(booking_data)
                    
                    return jsonify({
                        "status": "success",
                        "data": {
                            "type": "booking_updated",
                            "booking": optimized_data
                        }
                    })
                else:
                    logger.error(f"Error updating booking: {booking_response.text}")
                    return jsonify({
                        "status": "success",
                        "data": {
                            "type": "error",
                            "message": "I'm unable to update your booking at the moment. Please check the booking ID and try again."
                        }
                    })
            except requests.RequestException as req_error:
                logger.error(f"Request error updating booking: {str(req_error)}")
                return jsonify({
                    "status": "success",
                    "data": {
                        "type": "error",
                        "message": "I encountered a problem with our booking system. Please try again later or contact us directly by phone."
                    }
                })
                
        elif function_name == 'cancel_booking':
            # Cancel booking
            booking_id = arguments.get('booking_id')
            
            if not booking_id:
                return jsonify({
                    "status": "success",
                    "data": {
                        "type": "error",
                        "message": "I need your booking ID to cancel your reservation. Could you please provide it?"
                    }
                })
            
            logger.info(f"Cancelling booking with ID: {booking_id}")
            
            try:
                # Make request to booking API
                booking_response = requests.delete(
                    f"{request.url_root}api/knowledge/bookings?booking_id={booking_id}",
                    timeout=10
                )
                
                logger.info(f"Cancel booking response status: {booking_response.status_code}")
                
                if booking_response.status_code == 200:
                    return jsonify({
                        "status": "success",
                        "data": {
                            "type": "booking_cancelled",
                            "message": "Your booking has been successfully cancelled."
                        }
                    })
                else:
                    logger.error(f"Error cancelling booking: {booking_response.text}")
                    return jsonify({
                        "status": "success",
                        "data": {
                            "type": "error",
                            "message": "I'm unable to cancel your booking at the moment. Please check the booking ID and try again."
                        }
                    })
            except requests.RequestException as req_error:
                logger.error(f"Request error cancelling booking: {str(req_error)}")
                return jsonify({
                    "status": "success",
                    "data": {
                        "type": "error",
                        "message": "I encountered a problem with our booking system. Please try again later or contact us directly by phone."
                    }
                })
        else:
            logger.warning(f"Unknown function called: {function_name}")
            return jsonify({
                "status": "success",
                "data": {
                    "type": "general",
                    "message": "I'm not sure how to help with that specific request. I can provide information about our outlets, menu, answer FAQs, or help with bookings. How can I assist you today?"
                }
            })
            
    except Exception as e:
        logger.error(f"Error handling function call: {str(e)}")
        return jsonify({
            "status": "success",
            "data": "I apologize for the technical difficulties. I'm having trouble processing your request at the moment. Would you like to try a different question or maybe ask about our locations or menu?"
        })
