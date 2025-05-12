// Chat functionality for Barbeque Nation AI Assistant

// Chat state
let conversationState = 'greeting';
let conversationContext = {};
let chatHistory = [];
let currentPhone = '';

// Store API base URL
const API_BASE = window.location.origin;

// DOM elements - will be initialized when DOM is ready
let chatMessages;
let chatForm;
let userInput;
let userPhone;
let clearChatBtn;
let sampleQuestions;

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  console.log("DOM content loaded - initializing chat elements");
  
  // Initialize DOM elements after document is loaded
  chatMessages = document.getElementById('chat-messages');
  chatForm = document.getElementById('chat-form');
  userInput = document.getElementById('user-input');
  userPhone = document.getElementById('user-phone');
  clearChatBtn = document.getElementById('clear-chat');
  sampleQuestions = document.querySelectorAll('.sample-question');
  
  // Check if elements were found
  if (!chatMessages) {
    console.error("Chat messages container not found!");
  }
  
  if (!chatForm) {
    console.error("Chat form not found!");
  } else {
    initializeChat();
    setupEventListeners();
    loadChatHistory();
  }
});

// Initialize chat with greeting message
function initializeChat() {
  addMessage('Welcome to Barbeque Nation! I can help you with bookings, enquiries, and more for our outlets in Delhi and Bangalore. How may I assist you today?', 'assistant');
}

// Set up event listeners
function setupEventListeners() {
  // Form submission
  chatForm.addEventListener('submit', handleUserSubmit);
  
  // Sample questions
  sampleQuestions.forEach(question => {
    question.addEventListener('click', () => {
      userInput.value = question.textContent.trim();
      handleUserSubmit(new Event('submit'));
    });
  });
  
  // Clear chat button
  clearChatBtn.addEventListener('click', clearChat);
  
  // Save phone number when it changes
  userPhone.addEventListener('change', () => {
    currentPhone = userPhone.value;
    localStorage.setItem('bbq_user_phone', currentPhone);
  });
  
  // Handle beforeunload event to log conversation
  window.addEventListener('beforeunload', logConversation);
}

// Handle user message submission
async function handleUserSubmit(e) {
  e.preventDefault();
  
  const message = userInput.value.trim();
  if (!message) return;
  
  // Get phone number if set
  currentPhone = userPhone.value || currentPhone;
  
  // Add user message to chat
  addMessage(message, 'user');
  
  // Clear input
  userInput.value = '';
  
  // Show typing indicator
  showTypingIndicator();
  
  try {
    // Get the next state based on user input
    const stateTransition = await fetch(`${API_BASE}/api/conversation/transition`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        current_state: conversationState,
        user_input: message,
        context: conversationContext
      })
    });
    
    const stateData = await stateTransition.json();
    
    if (stateData.status === 'success') {
      // Update state and context
      conversationState = stateData.next_state;
      conversationContext = stateData.updated_context;
      
      // Use function calling to get response from knowledge base or perform actions
      const functionResponse = await handleFunctionCall(message);
      
      // Remove typing indicator
      removeTypingIndicator();
      
      // Add assistant response to chat
      addMessage(functionResponse, 'assistant');
      
      // Save chat history
      saveChatHistory();
    } else {
      // Handle error
      removeTypingIndicator();
      addMessage('I apologize, but I encountered an issue processing your request. Please try again.', 'assistant');
    }
  } catch (error) {
    console.error('Error processing message:', error);
    removeTypingIndicator();
    addMessage('I apologize, but there was an error processing your request. Please try again later.', 'assistant');
  }
}

// Handle function calling based on current state and user input
async function handleFunctionCall(userMessage) {
  // Default response if function calling fails
  let defaultResponse = "I'm here to help with information about Barbeque Nation. What would you like to know?";
  
  try {
    // Determine function to call based on state
    let functionName = 'query_knowledge_base';
    let functionArgs = { query: userMessage, type: 'general' };
    
    // Check if we're in a booking state
    if (conversationState === 'booking_enquiry' || conversationState === 'booking_confirmation') {
      // Check if we have all required booking details for confirmation
      if (conversationState === 'booking_confirmation' && 
          conversationContext.outlet && 
          conversationContext.booking_date && 
          conversationContext.booking_time && 
          conversationContext.guests && 
          conversationContext.customer_name && 
          conversationContext.phone) {
        // Complete booking
        functionName = 'create_booking';
        functionArgs = {
          outlet_id: conversationContext.outlet,
          date: conversationContext.booking_date,
          time: conversationContext.booking_time,
          guests: conversationContext.guests,
          customer_name: conversationContext.customer_name,
          phone: conversationContext.phone || currentPhone
        };
      } else {
        // Still collecting booking info
        functionName = 'query_knowledge_base';
        functionArgs = { query: userMessage, type: 'booking' };
      }
    } 
    // Check if we're in a modification state
    else if (conversationState === 'booking_modification' || 
             conversationState === 'booking_update_confirmation' || 
             conversationState === 'cancellation_confirmation') {
      // Handle cancellation
      if (conversationState === 'cancellation_confirmation' && conversationContext.booking_id) {
        functionName = 'cancel_booking';
        functionArgs = { booking_id: conversationContext.booking_id };
      } 
      // Handle update
      else if (conversationState === 'booking_update_confirmation' && conversationContext.booking_id) {
        functionName = 'update_booking';
        functionArgs = { 
          booking_id: conversationContext.booking_id,
          outlet_id: conversationContext.new_outlet,
          date: conversationContext.new_date,
          time: conversationContext.new_time,
          guests: conversationContext.new_guests
        };
      } else {
        // Still collecting modification info
        functionName = 'query_knowledge_base';
        functionArgs = { query: userMessage, type: 'booking_modification' };
      }
    } 
    // FAQ state
    else if (conversationState === 'faq_enquiry') {
      functionName = 'query_knowledge_base';
      functionArgs = { query: userMessage, type: 'faq' };
    }
    
    console.log("Making function call:", functionName, functionArgs);
    
    // Call function via API
    const response = await fetch(`${API_BASE}/api/conversation/retell/function-call`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: functionName,
        arguments: functionArgs
      })
    });
    
    const result = await response.json();
    console.log("API response:", result);
    
    if (result.status === 'success') {
      // Process the response based on the data type
      const data = result.data;
      
      if (!data) {
        return defaultResponse;
      }
      
      if (data.type === 'outlets') {
        return generateOutletsResponse(data.data || []);
      } else if (data.type === 'menu') {
        return generateMenuResponse(data.data || []);
      } else if (data.type === 'faq') {
        return generateFaqResponse(data.data || []);
      } else if (data.type === 'booking') {
        return data.message || "To make a reservation, I'll need your name, contact number, preferred date, time, and number of guests.";
      } else if (data.type === 'booking_created') {
        // Update context with booking ID
        conversationContext.booking_id = data.booking?.booking_id;
        return `Great! I've successfully booked your table. Here are the details:\n\nBooking ID: ${data.booking?.booking_id || 'N/A'}\nOutlet: ${data.booking?.outlet || 'N/A'}\nDate: ${data.booking?.date || 'N/A'}\nTime: ${data.booking?.time || 'N/A'}\nGuests: ${data.booking?.guests || 'N/A'}\n\nIs there anything else you'd like help with?`;
      } else if (data.type === 'booking_updated') {
        return `Your booking has been successfully updated. Here are the new details:\n\nBooking ID: ${data.booking?.booking_id || 'N/A'}\nOutlet: ${data.booking?.outlet || 'N/A'}\nDate: ${data.booking?.date || 'N/A'}\nTime: ${data.booking?.time || 'N/A'}\nGuests: ${data.booking?.guests || 'N/A'}\n\nIs there anything else you'd like help with?`;
      } else if (data.type === 'booking_cancelled') {
        return `Your booking has been successfully cancelled. Is there anything else I can help you with?`;
      } else if (data.type === 'error') {
        return data.message || "I'm sorry, I couldn't complete that request. Please try again.";
      } else if (data.type === 'general') {
        return data.message || defaultResponse;
      } else if (typeof data === 'string') {
        // Handle case where data is a string directly
        return data;
      } else {
        // Handle other response types or raw text
        return data.message || (typeof data === 'object' ? JSON.stringify(data) : String(data)) || defaultResponse;
      }
    } else {
      return result.message || defaultResponse;
    }
  } catch (error) {
    console.error('Function call error:', error);
    return "I apologize, but I'm having trouble processing your request right now. Could you please try again?";
  }
}

// Helper functions for response generation
function generateOutletsResponse(outlets) {
  if (!outlets || outlets.length === 0) {
    return "I don't have information about outlets matching your criteria.";
  }
  
  let response = "Here are the Barbeque Nation outlets you asked about:\n\n";
  
  outlets.forEach(outlet => {
    response += `📍 **${outlet.name}**\n`;
    response += `Address: ${outlet.address}\n`;
    response += `Phone: ${outlet.phone}\n`;
    response += `Hours: ${outlet.opening_hours}\n\n`;
  });
  
  return response + "Would you like to make a reservation at one of these locations?";
}

function generateMenuResponse(items) {
  if (!items || items.length === 0) {
    return "I don't have information about menu items matching your criteria.";
  }
  
  let response = "Here are the menu items you asked about:\n\n";
  
  items.forEach(item => {
    const vegIcon = item.is_vegetarian ? "🟢" : "🔴";
    response += `${vegIcon} **${item.name}** (${item.price})\n`;
    response += `${item.description}\n\n`;
  });
  
  return response + "Would you like to know about any other items or make a reservation?";
}

function generateFaqResponse(faqs) {
  if (!faqs || faqs.length === 0) {
    return "I don't have information about that in my knowledge base. Would you like to ask something else?";
  }
  
  // Take the most relevant FAQ (first one)
  const faq = faqs[0];
  return `${faq.answer}\n\nIs there anything else you'd like to know?`;
}

// UI functions
function addMessage(message, sender) {
  // Verify chat container exists
  if (!chatMessages) {
    console.error("Chat messages container not found");
    return;
  }
  
  const messageContainer = document.createElement('div');
  messageContainer.className = 'message-container';
  
  const messageElement = document.createElement('div');
  messageElement.className = `message message-${sender}`;
  
  // Format message text (handle markdown-like syntax)
  message = message.replace(/\n/g, '<br>');
  message = message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  message = message.replace(/\*(.*?)\*/g, '<em>$1</em>');
  
  // Set innerHTML instead of textContent to preserve formatting
  messageElement.innerHTML = message;
  
  const timeElement = document.createElement('div');
  timeElement.className = 'message-time';
  const now = new Date();
  timeElement.textContent = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`;
  
  messageElement.appendChild(timeElement);
  messageContainer.appendChild(messageElement);
  chatMessages.appendChild(messageContainer);
  
  // Save to chat history
  chatHistory.push({
    message,
    sender,
    timestamp: now
  });
  
  // Scroll to bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
  const typingContainer = document.createElement('div');
  typingContainer.className = 'message-container';
  typingContainer.id = 'typing-indicator';
  
  const typingElement = document.createElement('div');
  typingElement.className = 'message message-assistant';
  
  const loader = document.createElement('div');
  loader.className = 'loader';
  
  for (let i = 0; i < 3; i++) {
    const dot = document.createElement('div');
    loader.appendChild(dot);
  }
  
  typingElement.appendChild(loader);
  typingContainer.appendChild(typingElement);
  chatMessages.appendChild(typingContainer);
  
  // Scroll to bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
  const typingIndicator = document.getElementById('typing-indicator');
  if (typingIndicator) {
    typingIndicator.remove();
  }
}

// Chat history management
function saveChatHistory() {
  localStorage.setItem('bbq_chat_history', JSON.stringify(chatHistory));
  localStorage.setItem('bbq_conversation_state', conversationState);
  localStorage.setItem('bbq_conversation_context', JSON.stringify(conversationContext));
}

function loadChatHistory() {
  // Load chat history
  const savedHistory = localStorage.getItem('bbq_chat_history');
  const savedState = localStorage.getItem('bbq_conversation_state');
  const savedContext = localStorage.getItem('bbq_conversation_context');
  const savedPhone = localStorage.getItem('bbq_user_phone');
  
  if (savedHistory) {
    // Clear existing messages
    chatMessages.innerHTML = '';
    
    // Parse and display saved messages
    chatHistory = JSON.parse(savedHistory);
    chatHistory.forEach(item => {
      addMessage(item.message, item.sender);
    });
  }
  
  if (savedState) {
    conversationState = savedState;
  }
  
  if (savedContext) {
    conversationContext = JSON.parse(savedContext);
  }
  
  if (savedPhone) {
    currentPhone = savedPhone;
    userPhone.value = savedPhone;
  }
}

function clearChat() {
  // Clear chat UI
  chatMessages.innerHTML = '';
  
  // Reset state
  conversationState = 'greeting';
  conversationContext = {};
  chatHistory = [];
  
  // Clear localStorage
  localStorage.removeItem('bbq_chat_history');
  localStorage.removeItem('bbq_conversation_state');
  localStorage.removeItem('bbq_conversation_context');
  
  // Re-initialize chat
  initializeChat();
}

// Log conversation data when user leaves
async function logConversation() {
  // Only log if there are messages
  if (chatHistory.length <= 1) return; // Skip if only greeting message exists
  
  try {
    // Format conversation text for analysis
    const conversationText = chatHistory
      .map(item => `${item.sender.toUpperCase()}: ${item.message}`)
      .join('\n');
    
    // Send log data to server
    await fetch(`${API_BASE}/api/logs/log`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        modality: 'Chatbot',
        phone_number: currentPhone || 'unknown',
        conversation: conversationText,
        call_outcome: null, // Will be classified by backend
        customer_name: conversationContext.customer_name || null,
        booking_date: conversationContext.booking_date || null,
        booking_time: conversationContext.booking_time || null,
        guests: conversationContext.guests || null,
        outlet_name: conversationContext.outlet || null
      })
    });
  } catch (error) {
    console.error('Error logging conversation:', error);
  }
}
