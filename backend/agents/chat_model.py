"""
Mock implementation of ChatOpenAI for the Universal Shopping Assistant.
This implementation provides predefined responses based on user queries.
"""

from typing import List, Dict, Any, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

class ChatOpenAI:
    """
    Mock implementation of ChatOpenAI that returns predefined responses
    based on user queries.
    """
    
    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the mock ChatOpenAI model.
        
        Args:
            model: The model name (not used in mock)
            temperature: The temperature setting (not used in mock)
            api_key: The API key (not used in mock)
        """
        self.model = model
        self.temperature = temperature
        self.api_key = api_key
        print(f"[MOCK] Initialized ChatOpenAI with model: {model}")
    
    def invoke(self, messages: List[BaseMessage]) -> AIMessage:
        """
        Process the messages and return a predefined response based on the query.
        
        Args:
            messages: A list of messages in the conversation
            
        Returns:
            An AIMessage with the response
        """
        # Extract the last user message
        last_message = messages[-1]
        if isinstance(last_message, HumanMessage):
            query = last_message.content
        else:
            query = str(last_message)
        
        print(f"[MOCK] Processing user query: {query}")
        
        # Determine the type of query
        if "grocery" in query.lower():
            print("[MOCK] Detected grocery query type")
            response = self._generate_grocery_response(query)
        elif "tech" in query.lower() or "laptop" in query.lower() or "computer" in query.lower():
            print("[MOCK] Detected non-grocery query type: tech")
            response = self._generate_tech_response(query)
        elif "travel" in query.lower() or "vacation" in query.lower() or "trip" in query.lower():
            print("[MOCK] Detected non-grocery query type: travel")
            response = self._generate_travel_response(query)
        else:
            response = "I can help you with grocery shopping, tech product recommendations, travel planning, and financial advice. What would you like assistance with today?"
        
        return AIMessage(content=response)
    
    def _generate_grocery_response(self, query: str) -> str:
        """Generate a mock response for grocery-related queries."""
        return "Based on your preferences, I've created a grocery list with items from your local stores. The list includes fresh produce, dairy, and pantry staples, optimized for your dietary preferences and budget constraints."
    
    def _generate_tech_response(self, query: str) -> str:
        """Generate a mock response for tech-related queries."""
        return "I've analyzed the latest tech products matching your requirements. Here are the top recommendations based on performance, price, and user reviews. I've included options from different price ranges to give you flexibility in your decision."
    
    def _generate_travel_response(self, query: str) -> str:
        """Generate a mock response for travel-related queries."""
        return "I've put together a travel itinerary based on your preferences. The plan includes accommodations, transportation options, and activities that match your interests and budget. I've also included some local recommendations that tourists often miss."