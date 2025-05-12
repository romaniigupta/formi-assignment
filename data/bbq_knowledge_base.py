"""
This module contains the structured knowledge base for Barbeque Nation,
including outlet information, FAQ data, and menu details for Delhi and Bangalore locations.
"""

# Outlet information for Barbeque Nation in Delhi and Bangalore
bbq_outlets_info = [
    # Delhi Outlets
    {
        "id": "BBQD001",
        "name": "Barbeque Nation - Connaught Place",
        "address": "N-79, N Block, Connaught Place, New Delhi, Delhi 110001",
        "city": "Delhi",
        "phone": "011-40507777",
        "opening_hours": "12:00 PM - 11:00 PM",
        "cuisine": "North Indian, BBQ, Buffet",
        "price_range": "₹1,500 - ₹2,000 for two people",
        "capacity": 120,
        "features": ["Live BBQ", "Buffet", "Indoor Seating", "Air Conditioning"],
        "parking": "Valet Parking Available",
        "reservation_policy": "Reservations recommended, especially on weekends",
        "rating": 4.2,
        "location_coordinates": {
            "latitude": 28.6292,
            "longitude": 77.2182
        }
    },
    {
        "id": "BBQD002",
        "name": "Barbeque Nation - Nehru Place",
        "address": "Unit No. 64, 4th Floor, Eros International Building, Nehru Place, New Delhi, Delhi 110019",
        "city": "Delhi",
        "phone": "011-40507778",
        "opening_hours": "12:00 PM - 11:00 PM",
        "cuisine": "North Indian, BBQ, Buffet",
        "price_range": "₹1,400 - ₹1,800 for two people",
        "capacity": 150,
        "features": ["Live BBQ", "Buffet", "Indoor Seating", "Private Dining Area"],
        "parking": "Available at Nehru Place Mall",
        "reservation_policy": "Reservations recommended",
        "rating": 4.0,
        "location_coordinates": {
            "latitude": 28.5491,
            "longitude": 77.2533
        }
    },
    {
        "id": "BBQD003",
        "name": "Barbeque Nation - Vasant Kunj",
        "address": "2nd Floor, DLF Promenade Mall, Vasant Kunj, New Delhi, Delhi 110070",
        "city": "Delhi",
        "phone": "011-40507779",
        "opening_hours": "12:00 PM - 11:00 PM",
        "cuisine": "North Indian, BBQ, Buffet",
        "price_range": "₹1,600 - ₹2,200 for two people",
        "capacity": 180,
        "features": ["Live BBQ", "Buffet", "Indoor Seating", "Birthday Celebrations"],
        "parking": "Mall Parking Available",
        "reservation_policy": "Reservations recommended, especially on weekends",
        "rating": 4.3,
        "location_coordinates": {
            "latitude": 28.5219,
            "longitude": 77.1588
        }
    },
    
    # Bangalore Outlets
    {
        "id": "BBQB001",
        "name": "Barbeque Nation - Koramangala",
        "address": "90/4, 3rd Floor, Outer Ring Road, Koramangala, Bengaluru, Karnataka 560095",
        "city": "Bangalore",
        "phone": "080-41157777",
        "opening_hours": "12:00 PM - 11:30 PM",
        "cuisine": "North Indian, BBQ, Buffet",
        "price_range": "₹1,500 - ₹1,900 for two people",
        "capacity": 160,
        "features": ["Live BBQ", "Buffet", "Indoor Seating", "Corporate Events"],
        "parking": "Available",
        "reservation_policy": "Reservations recommended",
        "rating": 4.4,
        "location_coordinates": {
            "latitude": 12.9346,
            "longitude": 77.6140
        }
    },
    {
        "id": "BBQB002",
        "name": "Barbeque Nation - Indiranagar",
        "address": "607, 2nd Floor, 12th Main Road, HAL 2nd Stage, Indiranagar, Bengaluru, Karnataka 560008",
        "city": "Bangalore",
        "phone": "080-41157778",
        "opening_hours": "12:00 PM - 11:30 PM",
        "cuisine": "North Indian, BBQ, Buffet",
        "price_range": "₹1,600 - ₹2,000 for two people",
        "capacity": 140,
        "features": ["Live BBQ", "Buffet", "Indoor Seating", "Birthday Celebrations"],
        "parking": "Valet Parking Available",
        "reservation_policy": "Reservations recommended, especially on weekends",
        "rating": 4.3,
        "location_coordinates": {
            "latitude": 12.9690,
            "longitude": 77.6442
        }
    },
    {
        "id": "BBQB003",
        "name": "Barbeque Nation - Whitefield",
        "address": "2nd Floor, Phoenix Marketcity, Whitefield Road, Mahadevapura, Bengaluru, Karnataka 560048",
        "city": "Bangalore",
        "phone": "080-41157779",
        "opening_hours": "12:00 PM - 11:00 PM",
        "cuisine": "North Indian, BBQ, Buffet",
        "price_range": "₹1,500 - ₹1,900 for two people",
        "capacity": 170,
        "features": ["Live BBQ", "Buffet", "Indoor Seating", "Kid-friendly"],
        "parking": "Mall Parking Available",
        "reservation_policy": "Reservations recommended",
        "rating": 4.1,
        "location_coordinates": {
            "latitude": 12.9959,
            "longitude": 77.7292
        }
    }
]

# FAQ information for Barbeque Nation
bbq_faq_info = [
    # General FAQs
    {
        "id": "FAQ001",
        "question": "What is the concept of Barbeque Nation?",
        "answer": "Barbeque Nation is a unique dining experience where each table is equipped with a live grill. Guests can grill their own starters with marinades of their choice and enjoy unlimited servings of these along with a full buffet spread that includes main courses, soups, salads, and desserts.",
        "category": "general"
    },
    {
        "id": "FAQ002",
        "question": "How does the live grill at the table work?",
        "answer": "Each table at Barbeque Nation has a built-in grill in the center. Our staff will bring pre-marinated, skewered meats and vegetables that you can place on your table's grill. You can adjust the cooking to your preference, and staff are always available to assist. It's a fun, interactive dining experience!",
        "category": "general"
    },
    {
        "id": "FAQ003",
        "question": "Is the buffet unlimited?",
        "answer": "Yes, our buffet is unlimited. You can enjoy unlimited servings of starters, main course items, soups, salads, and desserts during your dining session.",
        "category": "general"
    },
    
    # Booking FAQs
    {
        "id": "FAQ004",
        "question": "How can I make a reservation?",
        "answer": "You can make a reservation by calling your preferred outlet directly, booking online through our website, using our mobile app, or through third-party platforms like Zomato or Dineout.",
        "category": "booking"
    },
    {
        "id": "FAQ005",
        "question": "Do I need a reservation, or can I walk in?",
        "answer": "While walk-ins are accepted, we strongly recommend making a reservation, especially for dinner service and on weekends, as we tend to be quite busy during these times.",
        "category": "booking"
    },
    {
        "id": "FAQ006",
        "question": "How far in advance should I make a reservation?",
        "answer": "For weekday lunch, 1-2 days in advance is usually sufficient. For dinner and weekends, we recommend booking 3-4 days in advance. For large groups or special occasions, booking a week in advance is advisable.",
        "category": "booking"
    },
    {
        "id": "FAQ007",
        "question": "Can I modify or cancel my reservation?",
        "answer": "Yes, you can modify or cancel your reservation. We request that you inform us at least 2 hours before your scheduled time. For groups of 10 or more, please notify us 24 hours in advance.",
        "category": "booking"
    },
    
    # Menu and Pricing FAQs
    {
        "id": "FAQ008",
        "question": "What is the average cost per person?",
        "answer": "The average cost per person ranges from ₹800 to ₹1,100 plus taxes, depending on the day of the week and the specific meal (lunch or dinner). Weekend dinner is typically priced higher than weekday lunch.",
        "category": "pricing"
    },
    {
        "id": "FAQ009",
        "question": "Are there different prices for lunch and dinner?",
        "answer": "Yes, dinner is usually priced slightly higher than lunch. Additionally, weekend prices (Friday to Sunday) are slightly higher than weekday prices (Monday to Thursday).",
        "category": "pricing"
    },
    {
        "id": "FAQ010",
        "question": "Do you have different pricing for children?",
        "answer": "Yes, we offer special pricing for children. Kids between the ages of 5-10 years are charged at approximately 60% of the adult price. Children under 5 years dine free of charge when accompanied by a paying adult.",
        "category": "pricing"
    },
    {
        "id": "FAQ011",
        "question": "What types of food do you serve?",
        "answer": "We serve a variety of cuisines including North Indian, Mughlai, Chinese, and Continental. Our menu includes vegetarian and non-vegetarian options with a wide selection of starters, main courses, and desserts.",
        "category": "menu"
    },
    {
        "id": "FAQ012",
        "question": "Do you have vegetarian options?",
        "answer": "Yes, we have extensive vegetarian options in both our starter and main course selections. Our vegetarian dishes are prepared separately from non-vegetarian items to maintain their integrity.",
        "category": "menu"
    },
    {
        "id": "FAQ013",
        "question": "Do you serve alcohol?",
        "answer": "Yes, we have a full bar with a selection of domestic and imported alcoholic beverages. Please note that alcohol is charged separately and is not included in the buffet price.",
        "category": "menu"
    },
    
    # Special Occasions FAQs
    {
        "id": "FAQ014",
        "question": "Can I celebrate a birthday or anniversary at Barbeque Nation?",
        "answer": "Absolutely! We offer special celebration packages for birthdays, anniversaries, and other special occasions. We can arrange for a cake, special decorations, and even a small celebration with our staff singing for the occasion. Please inform us at the time of booking.",
        "category": "special_occasions"
    },
    {
        "id": "FAQ015",
        "question": "Can I bring my own cake?",
        "answer": "Yes, you can bring your own cake. We charge a small cake-cutting fee, which varies by location. Please inform the staff in advance if you plan to bring a cake.",
        "category": "special_occasions"
    },
    {
        "id": "FAQ016",
        "question": "Can I host a large group or corporate event?",
        "answer": "Yes, we cater to large groups and corporate events. We offer special group packages and can customize the menu and setup based on your requirements. For groups larger than 15 people, please contact our events team for special arrangements.",
        "category": "special_occasions"
    },
    
    # Other FAQs
    {
        "id": "FAQ017",
        "question": "Is there a time limit for dining?",
        "answer": "Yes, there is a standard dining time of 90 minutes for regular meals. For large groups or during peak hours, this may be slightly adjusted. Our staff will inform you about any time constraints when you arrive.",
        "category": "other"
    },
    {
        "id": "FAQ018",
        "question": "Is parking available?",
        "answer": "Parking availability varies by location. Most of our outlets in malls have access to mall parking. Some standalone outlets offer valet parking. Please check with your specific outlet for parking details.",
        "category": "other"
    },
    {
        "id": "FAQ019",
        "question": "Do you have any loyalty programs or discounts?",
        "answer": "Yes, we have a loyalty program called 'BBQ Addicts' that offers points for every visit, which can be redeemed for discounts on future visits. We also run seasonal promotions and discounts for early dining on weekdays.",
        "category": "other"
    },
    {
        "id": "FAQ020",
        "question": "Are pets allowed?",
        "answer": "Unfortunately, pets are not allowed in our restaurants, with the exception of service animals.",
        "category": "other"
    }
]

# Menu information for Barbeque Nation
bbq_menu_info = [
    # Starters - Vegetarian
    {
        "id": "MENUSV001",
        "name": "Paneer Tikka",
        "description": "Marinated cottage cheese cubes, grilled to perfection with a smoky flavor",
        "category": "starters",
        "is_vegetarian": True,
        "price": "₹250",
        "spice_level": "Medium",
        "contains": ["Dairy", "Gluten"],
        "availability": "All outlets"
    },
    {
        "id": "MENUSV002",
        "name": "Crispy Corn",
        "description": "Crunchy sweet corn kernels tossed with spices and herbs",
        "category": "starters",
        "is_vegetarian": True,
        "price": "₹220",
        "spice_level": "Medium",
        "contains": ["Gluten"],
        "availability": "All outlets"
    },
    {
        "id": "MENUSV003",
        "name": "Mushroom Tikka",
        "description": "Button mushrooms marinated in spices and grilled",
        "category": "starters",
        "is_vegetarian": True,
        "price": "₹240",
        "spice_level": "Mild",
        "contains": ["Dairy"],
        "availability": "All outlets"
    },
    {
        "id": "MENUSV004",
        "name": "Cajun Spice Potato",
        "description": "Baby potatoes marinated with Cajun spices and grilled",
        "category": "starters",
        "is_vegetarian": True,
        "price": "₹200",
        "spice_level": "Medium",
        "contains": [],
        "availability": "All outlets"
    },
    
    # Starters - Non-Vegetarian
    {
        "id": "MENUSNV001",
        "name": "Chicken Tikka",
        "description": "Boneless chicken marinated in yogurt and spices, grilled to perfection",
        "category": "starters",
        "is_vegetarian": False,
        "price": "₹320",
        "spice_level": "Medium",
        "contains": ["Dairy"],
        "availability": "All outlets"
    },
    {
        "id": "MENUSNV002",
        "name": "Fish Tikka",
        "description": "Boneless fish marinated with aromatic Indian spices and grilled",
        "category": "starters",
        "is_vegetarian": False,
        "price": "₹350",
        "spice_level": "Medium",
        "contains": ["Fish"],
        "availability": "All outlets"
    },
    {
        "id": "MENUSNV003",
        "name": "Seekh Kebab",
        "description": "Minced lamb mixed with herbs and spices, grilled on skewers",
        "category": "starters",
        "is_vegetarian": False,
        "price": "₹370",
        "spice_level": "High",
        "contains": [],
        "availability": "All outlets"
    },
    {
        "id": "MENUSNV004",
        "name": "Garlic Pepper Prawns",
        "description": "Prawns marinated with garlic and black pepper, grilled to perfection",
        "category": "starters",
        "is_vegetarian": False,
        "price": "₹390",
        "spice_level": "Medium",
        "contains": ["Shellfish"],
        "availability": "All outlets"
    },
    
    # Main Course - Vegetarian
    {
        "id": "MENUMCV001",
        "name": "Paneer Butter Masala",
        "description": "Cottage cheese cubes cooked in a rich tomato and butter gravy",
        "category": "main course",
        "is_vegetarian": True,
        "price": "₹280",
        "spice_level": "Medium",
        "contains": ["Dairy", "Nuts"],
        "availability": "All outlets"
    },
    {
        "id": "MENUMCV002",
        "name": "Dal Makhani",
        "description": "Black lentils and kidney beans slow-cooked with butter and cream",
        "category": "main course",
        "is_vegetarian": True,
        "price": "₹250",
        "spice_level": "Mild",
        "contains": ["Dairy"],
        "availability": "All outlets"
    },
    {
        "id": "MENUMCV003",
        "name": "Veg Biryani",
        "description": "Fragrant basmati rice cooked with mixed vegetables and aromatic spices",
        "category": "main course",
        "is_vegetarian": True,
        "price": "₹270",
        "spice_level": "Medium",
        "contains": [],
        "availability": "All outlets"
    },
    
    # Main Course - Non-Vegetarian
    {
        "id": "MENUMCNV001",
        "name": "Butter Chicken",
        "description": "Tandoori chicken cooked in a rich tomato, butter, and cream sauce",
        "category": "main course",
        "is_vegetarian": False,
        "price": "₹340",
        "spice_level": "Medium",
        "contains": ["Dairy"],
        "availability": "All outlets"
    },
    {
        "id": "MENUMCNV002",
        "name": "Chicken Biryani",
        "description": "Fragrant basmati rice cooked with chicken and aromatic spices",
        "category": "main course",
        "is_vegetarian": False,
        "price": "₹320",
        "spice_level": "Medium",
        "contains": [],
        "availability": "All outlets"
    },
    {
        "id": "MENUMCNV003",
        "name": "Mutton Rogan Josh",
        "description": "Tender mutton pieces cooked in a rich gravy with Kashmiri spices",
        "category": "main course",
        "is_vegetarian": False,
        "price": "₹380",
        "spice_level": "High",
        "contains": [],
        "availability": "All outlets"
    },
    
    # Desserts
    {
        "id": "MENUDS001",
        "name": "Gulab Jamun",
        "description": "Soft milk solids dumplings soaked in sugar syrup",
        "category": "desserts",
        "is_vegetarian": True,
        "price": "₹150",
        "spice_level": "None",
        "contains": ["Dairy", "Gluten"],
        "availability": "All outlets"
    },
    {
        "id": "MENUDS002",
        "name": "Chocolate Brownie",
        "description": "Warm chocolate brownie served with vanilla ice cream",
        "category": "desserts",
        "is_vegetarian": True,
        "price": "₹180",
        "spice_level": "None",
        "contains": ["Dairy", "Gluten", "Eggs"],
        "availability": "All outlets"
    },
    {
        "id": "MENUDS003",
        "name": "Kulfi Falooda",
        "description": "Traditional Indian ice cream served with vermicelli and rose syrup",
        "category": "desserts",
        "is_vegetarian": True,
        "price": "₹170",
        "spice_level": "None",
        "contains": ["Dairy"],
        "availability": "All outlets"
    },
    
    # Beverages
    {
        "id": "MENUBV001",
        "name": "Fresh Lime Soda",
        "description": "Refreshing lime juice with soda water, sweetened or salted",
        "category": "beverages",
        "is_vegetarian": True,
        "price": "₹120",
        "spice_level": "None",
        "contains": [],
        "availability": "All outlets"
    },
    {
        "id": "MENUBV002",
        "name": "Masala Chai",
        "description": "Traditional Indian spiced tea",
        "category": "beverages",
        "is_vegetarian": True,
        "price": "₹100",
        "spice_level": "None",
        "contains": ["Dairy"],
        "availability": "All outlets"
    },
    {
        "id": "MENUBV003",
        "name": "Mango Lassi",
        "description": "Yogurt-based drink blended with mango pulp and sugar",
        "category": "beverages",
        "is_vegetarian": True,
        "price": "₹140",
        "spice_level": "None",
        "contains": ["Dairy"],
        "availability": "All outlets"
    }
]
