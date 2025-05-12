import re
import json
import logging
from jinja2 import Template

# Configure logging
logger = logging.getLogger(__name__)

class StateTransition:
    """
    Handles state transitions and prompt management for the conversation flow.
    """
    
    def __init__(self):
        """Initialize the state transition manager with state definitions."""
        # Define states and their transitions
        self.states = {
            # Greeting state - initial state for all conversations
            "greeting": {
                "prompt": """
                You are a customer service assistant for Barbeque Nation, a popular chain of barbecue restaurants in India.
                Your name is BBQ Assistant. You are helping customers with enquiries, bookings, and updates for Barbeque Nation
                outlets in Delhi and Bangalore.
                
                Keep your responses friendly, helpful, and concise. Your goal is to assist customers with:
                1. Answering questions about Barbeque Nation (locations, menu, pricing, etc.)
                2. Creating new table bookings
                3. Modifying or cancelling existing bookings
                
                In this state, you should greet the customer warmly and ask how you can help them today.
                """,
                "transitions": {
                    "booking_enquiry": ["book", "reserve", "table", "reservation"],
                    "faq_enquiry": ["question", "faq", "menu", "price", "location", "hour", "special", "offer"],
                    "booking_modification": ["change", "modify", "update", "cancel", "existing", "booking"]
                }
            },
            
            # FAQ enquiry state - handling general questions
            "faq_enquiry": {
                "prompt": """
                You are now handling a general enquiry about Barbeque Nation.
                
                Current context:
                {% if outlet %}
                - Customer is asking about the {{ outlet }} outlet
                {% endif %}
                {% if query_topic %}
                - Their query is related to {{ query_topic }}
                {% endif %}
                
                Answer the customer's question based on your knowledge of Barbeque Nation. If you need specific information,
                use the query_knowledge_base function to retrieve accurate details.
                
                Be helpful, specific, and conversational. If you're unsure about any information, it's better to acknowledge
                that and offer to check rather than provide incorrect information.
                """,
                "transitions": {
                    "booking_enquiry": ["book", "reserve", "table", "reservation", "make booking"],
                    "booking_modification": ["change", "modify", "update", "cancel", "existing", "booking"],
                    "goodbye": ["thank", "thanks", "bye", "goodbye", "that's all"]
                }
            },
            
            # Booking enquiry state - handling new booking requests
            "booking_enquiry": {
                "prompt": """
                You are now helping a customer make a new booking at Barbeque Nation.
                
                Current booking information:
                {% if outlet %}
                - Outlet: {{ outlet }}
                {% else %}
                - Outlet: Not specified yet
                {% endif %}
                {% if booking_date %}
                - Date: {{ booking_date }}
                {% else %}
                - Date: Not specified yet
                {% endif %}
                {% if booking_time %}
                - Time: {{ booking_time }}
                {% else %}
                - Time: Not specified yet
                {% endif %}
                {% if guests %}
                - Number of guests: {{ guests }}
                {% else %}
                - Number of guests: Not specified yet
                {% endif %}
                {% if customer_name %}
                - Name: {{ customer_name }}
                {% else %}
                - Name: Not specified yet
                {% endif %}
                {% if phone %}
                - Phone: {{ phone }}
                {% else %}
                - Phone: Not specified yet
                {% endif %}
                
                Guide the customer through the booking process by collecting all required information.
                If any information is missing, politely ask for it. Once all details are collected,
                use the create_booking function to finalize the reservation.
                
                If the customer asks about outlet options, menu, or other information during the booking process,
                use the query_knowledge_base function to provide accurate information.
                """,
                "transitions": {
                    "booking_confirmation": ["all_details_collected"],
                    "faq_enquiry": ["question", "faq", "tell me about"],
                    "goodbye": ["cancel", "never mind", "stop", "quit"]
                }
            },
            
            # Booking confirmation state - confirming booking details
            "booking_confirmation": {
                "prompt": """
                You are now confirming the booking details with the customer.
                
                Booking details:
                - Outlet: {{ outlet }}
                - Date: {{ booking_date }}
                - Time: {{ booking_time }}
                - Number of guests: {{ guests }}
                - Name: {{ customer_name }}
                - Phone: {{ phone }}
                
                Confirm these details with the customer. Ask if everything is correct.
                If they confirm, use the create_booking function to finalize the reservation.
                If they want to make changes, update the relevant information and ask for confirmation again.
                """,
                "transitions": {
                    "booking_successful": ["confirm", "yes", "correct", "that's right"],
                    "booking_enquiry": ["change", "modify", "no", "incorrect", "wrong"],
                    "goodbye": ["cancel", "never mind", "stop", "quit"]
                }
            },
            
            # Booking successful state - booking has been created
            "booking_successful": {
                "prompt": """
                The booking has been successfully created.
                
                Booking details:
                - Booking ID: {{ booking_id }}
                - Outlet: {{ outlet }}
                - Date: {{ booking_date }}
                - Time: {{ booking_time }}
                - Number of guests: {{ guests }}
                - Name: {{ customer_name }}
                - Phone: {{ phone }}
                
                Confirm the successful booking with the customer. Provide the booking ID and important
                information about their reservation. Ask if there's anything else they need help with.
                """,
                "transitions": {
                    "faq_enquiry": ["question", "enquiry", "tell me about"],
                    "booking_modification": ["change", "modify", "update"],
                    "goodbye": ["no", "thank", "thanks", "bye", "goodbye", "that's all"]
                }
            },
            
            # Booking modification state - handling changes to existing bookings
            "booking_modification": {
                "prompt": """
                You are now helping a customer modify or cancel an existing booking.
                
                {% if booking_id %}
                Current booking ID: {{ booking_id }}
                {% else %}
                No booking ID provided yet.
                {% endif %}
                
                {% if modification_type %}
                Modification type: {{ modification_type }}
                {% else %}
                Modification type not specified yet.
                {% endif %}
                
                First, ask for the booking ID if not provided. Then, determine what changes the customer wants to make
                (change date/time, change number of guests, or cancel booking).
                
                For modifications, collect the new details and use the update_booking function.
                For cancellations, confirm the customer wants to cancel, and then use the cancel_booking function.
                """,
                "transitions": {
                    "booking_update_confirmation": ["modification_details_collected"],
                    "cancellation_confirmation": ["cancel", "cancellation"],
                    "faq_enquiry": ["question", "faq", "tell me about"],
                    "goodbye": ["never mind", "stop", "quit"]
                }
            },
            
            # Booking update confirmation state - confirming modification details
            "booking_update_confirmation": {
                "prompt": """
                You are now confirming the booking modification details with the customer.
                
                Original booking ID: {{ booking_id }}
                
                Changes to be made:
                {% if new_date %}
                - New date: {{ new_date }}
                {% endif %}
                {% if new_time %}
                - New time: {{ new_time }}
                {% endif %}
                {% if new_guests %}
                - New number of guests: {{ new_guests }}
                {% endif %}
                {% if new_outlet %}
                - New outlet: {{ new_outlet }}
                {% endif %}
                
                Confirm these changes with the customer. Ask if everything is correct.
                If they confirm, use the update_booking function to apply the changes.
                If they want to make further changes, update the relevant information and ask for confirmation again.
                """,
                "transitions": {
                    "booking_update_successful": ["confirm", "yes", "correct", "that's right"],
                    "booking_modification": ["change", "modify", "no", "incorrect", "wrong"],
                    "goodbye": ["cancel", "never mind", "stop", "quit"]
                }
            },
            
            # Booking update successful state - modifications have been applied
            "booking_update_successful": {
                "prompt": """
                The booking has been successfully updated.
                
                Updated booking details:
                - Booking ID: {{ booking_id }}
                {% if outlet %}
                - Outlet: {{ outlet }}
                {% endif %}
                {% if booking_date %}
                - Date: {{ booking_date }}
                {% endif %}
                {% if booking_time %}
                - Time: {{ booking_time }}
                {% endif %}
                {% if guests %}
                - Number of guests: {{ guests }}
                {% endif %}
                
                Confirm the successful update with the customer. Provide the updated details
                and ask if there's anything else they need help with.
                """,
                "transitions": {
                    "faq_enquiry": ["question", "enquiry", "tell me about"],
                    "booking_modification": ["change", "modify", "update"],
                    "goodbye": ["no", "thank", "thanks", "bye", "goodbye", "that's all"]
                }
            },
            
            # Cancellation confirmation state - confirming booking cancellation
            "cancellation_confirmation": {
                "prompt": """
                You are now confirming the cancellation of a booking.
                
                Booking ID to cancel: {{ booking_id }}
                
                Confirm with the customer that they want to cancel this booking.
                Remind them that cancellation is permanent and cannot be undone.
                
                If they confirm, use the cancel_booking function to process the cancellation.
                If they change their mind, return to the appropriate previous state.
                """,
                "transitions": {
                    "cancellation_successful": ["confirm", "yes", "sure", "proceed"],
                    "booking_modification": ["no", "wait", "stop", "keep", "don't cancel"],
                    "goodbye": ["never mind", "quit"]
                }
            },
            
            # Cancellation successful state - booking has been cancelled
            "cancellation_successful": {
                "prompt": """
                The booking has been successfully cancelled.
                
                Cancelled booking ID: {{ booking_id }}
                
                Confirm the successful cancellation with the customer.
                Thank them for their understanding and ask if there's anything else they need help with.
                """,
                "transitions": {
                    "booking_enquiry": ["new booking", "book", "reserve"],
                    "faq_enquiry": ["question", "enquiry", "tell me about"],
                    "goodbye": ["no", "thank", "thanks", "bye", "goodbye", "that's all"]
                }
            },
            
            # Goodbye state - end of conversation
            "goodbye": {
                "prompt": """
                The conversation is coming to an end.
                
                Thank the customer for contacting Barbeque Nation. Express your appreciation for
                their interest and offer a warm, friendly goodbye.
                
                If appropriate, remind them of any booking details or important information
                discussed during the conversation.
                """,
                "transitions": {
                    "greeting": ["help", "another", "question", "more"]
                }
            }
        }
    
    def get_state_prompt(self, state_name):
        """
        Get the prompt template for a given state.
        
        Args:
            state_name (str): Name of the state to get prompt for
            
        Returns:
            str: Prompt template for the state
        """
        if state_name in self.states:
            return self.states[state_name].get('prompt', '')
        else:
            logger.warning(f"Unknown state: {state_name}, falling back to greeting")
            return self.states['greeting'].get('prompt', '')
    
    def determine_next_state(self, current_state, user_input, context):
        """
        Determine the next state based on current state and user input.
        
        Args:
            current_state (str): Current state name
            user_input (str): User's input text
            context (dict): Current conversation context
            
        Returns:
            tuple: (next_state, updated_context)
        """
        if current_state not in self.states:
            logger.warning(f"Unknown current state: {current_state}, resetting to greeting")
            return 'greeting', context
            
        # Get possible transitions
        transitions = self.states[current_state].get('transitions', {})
        
        # Check for special transition conditions
        if current_state == 'booking_enquiry':
            # Check if all required booking details are collected
            required_fields = ['outlet', 'booking_date', 'booking_time', 'guests', 'customer_name', 'phone']
            all_collected = all(field in context and context[field] for field in required_fields)
            
            if all_collected and 'all_details_collected' in transitions:
                return transitions['all_details_collected'], context
                
        if current_state == 'booking_modification':
            # Check if all modification details are collected
            if 'booking_id' in context and 'modification_type' in context:
                if context['modification_type'] == 'cancel':
                    if 'cancellation' in transitions:
                        return transitions['cancellation'], context
                elif any(field in context for field in ['new_date', 'new_time', 'new_guests', 'new_outlet']):
                    if 'modification_details_collected' in transitions:
                        return transitions['modification_details_collected'], context
        
        # Check for keyword-based transitions
        user_input_lower = user_input.lower()
        for next_state, keywords in transitions.items():
            for keyword in keywords:
                if keyword.lower() in user_input_lower:
                    # Update context based on state transitions
                    updated_context = self._update_context(current_state, next_state, user_input, context)
                    return next_state, updated_context
                    
        # If no transition found, stay in current state
        # But still update the context with any new information
        updated_context = self._update_context(current_state, current_state, user_input, context)
        return current_state, updated_context
    
    def _update_context(self, current_state, next_state, user_input, context):
        """
        Update the context based on user input and state transition.
        
        Args:
            current_state (str): Current state name
            next_state (str): Next state name
            user_input (str): User's input text
            context (dict): Current conversation context
            
        Returns:
            dict: Updated context
        """
        # Create a copy of the context to update
        updated_context = context.copy()
        
        # Extract relevant information based on the current state and user input
        if current_state == 'greeting' and next_state == 'faq_enquiry':
            # Extract query topic from user input
            topics = ['menu', 'price', 'location', 'hours', 'special', 'offer']
            for topic in topics:
                if topic in user_input.lower():
                    updated_context['query_topic'] = topic
                    break
            
            # Extract outlet if mentioned
            outlets = ['Delhi', 'Bangalore', 'Connaught Place', 'Nehru Place', 'Vasant Kunj', 
                      'Koramangala', 'Indiranagar', 'Whitefield']
            for outlet in outlets:
                if outlet.lower() in user_input.lower():
                    updated_context['outlet'] = outlet
                    break
        
        elif current_state == 'greeting' and next_state == 'booking_enquiry':
            # Extract initial booking details if provided
            self._extract_booking_details(user_input, updated_context)
        
        elif current_state == 'greeting' and next_state == 'booking_modification':
            # Extract booking ID if provided
            booking_match = re.search(r'booking (?:id|ID|number|#)?\s*:?\s*([A-Z0-9]+)', user_input)
            if booking_match:
                updated_context['booking_id'] = booking_match.group(1)
            
            # Extract modification type
            if 'cancel' in user_input.lower():
                updated_context['modification_type'] = 'cancel'
            elif any(word in user_input.lower() for word in ['change', 'modify', 'update']):
                updated_context['modification_type'] = 'update'
        
        elif current_state == 'booking_enquiry' and next_state == 'booking_enquiry':
            # Continue collecting booking details
            self._extract_booking_details(user_input, updated_context)
        
        elif current_state == 'booking_modification' and next_state == 'booking_modification':
            # Continue collecting modification details
            if 'booking_id' not in updated_context:
                booking_match = re.search(r'(?:booking (?:id|ID|number|#)?\s*:?\s*)?([A-Z0-9]+)', user_input)
                if booking_match:
                    updated_context['booking_id'] = booking_match.group(1)
            
            if 'modification_type' not in updated_context:
                if 'cancel' in user_input.lower():
                    updated_context['modification_type'] = 'cancel'
                elif any(word in user_input.lower() for word in ['change', 'modify', 'update']):
                    updated_context['modification_type'] = 'update'
            
            # If updating, extract new details
            if updated_context.get('modification_type') == 'update':
                self._extract_booking_details(user_input, updated_context, prefix='new_')
        
        return updated_context
    
    def _extract_booking_details(self, text, context, prefix=''):
        """
        Extract booking details from text and update context.
        
        Args:
            text (str): Text to extract details from
            context (dict): Context to update
            prefix (str): Prefix for context keys (for update scenarios)
        """
        # Extract date
        date_key = f'{prefix}booking_date'
        date_match = re.search(r'(?:date|on|for|)\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}-\d{2}-\d{2})', text)
        if date_match and date_key not in context:
            context[date_key] = date_match.group(1)
        
        # Extract time
        time_key = f'{prefix}booking_time'
        time_match = re.search(r'(?:time|at)\s*:?\s*(\d{1,2}:\d{2}(?:\s*(?:am|pm))?|\d{1,2}\s*(?:am|pm))', text, re.IGNORECASE)
        if time_match and time_key not in context:
            context[time_key] = time_match.group(1)
        
        # Extract number of guests
        guests_key = f'{prefix}guests'
        guests_match = re.search(r'(?:for|with|)\s*(\d+)\s*(?:people|persons|guests|pax)', text, re.IGNORECASE)
        if guests_match and guests_key not in context:
            context[guests_key] = guests_match.group(1)
        
        # Extract customer name
        name_key = f'{prefix}customer_name'
        name_match = re.search(r'(?:name|this is|I am|I\'m)\s+(?:is\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})', text)
        if name_match and name_key not in context:
            context[name_key] = name_match.group(1)
        
        # Extract phone number
        phone_key = f'{prefix}phone'
        phone_match = re.search(r'(?:phone|number|contact|call|)\s*(?:is|at|:)?\s*((?:\+91|0)?[6-9][0-9]{9})', text)
        if phone_match and phone_key not in context:
            context[phone_key] = phone_match.group(1)
        
        # Extract outlet
        outlet_key = f'{prefix}outlet'
        outlets = {
            'delhi': 'Barbeque Nation Delhi',
            'connaught': 'Barbeque Nation Connaught Place',
            'nehru': 'Barbeque Nation Nehru Place',
            'vasant': 'Barbeque Nation Vasant Kunj',
            'bangalore': 'Barbeque Nation Bangalore',
            'koramangala': 'Barbeque Nation Koramangala', 
            'indiranagar': 'Barbeque Nation Indiranagar',
            'whitefield': 'Barbeque Nation Whitefield'
        }
        
        for key, value in outlets.items():
            if key.lower() in text.lower() and outlet_key not in context:
                context[outlet_key] = value
                break
