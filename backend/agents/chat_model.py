"""
Mock implementation of ChatOpenAI to avoid compatibility issues.
"""

from typing import Any, Dict, List, Optional, Union


class ChatOpenAI:
    """
    Mock implementation of ChatOpenAI that returns predefined responses.
    This helps avoid dependency issues with different versions of OpenAI and LangChain.
    """
    
    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        api_key: Optional[str] = None,
        **kwargs
    ):
        self.model = model
        self.temperature = temperature
        self.api_key = api_key
        print(f"[MOCK] Initialized ChatOpenAI with model: {model}")
    
    def invoke(self, messages: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """Mock implementation that returns a predefined response."""
        # Extract the last user message if available
        user_message = ""
        for message in reversed(messages):
            if message.get("role") == "user":
                user_message = message.get("content", "")
                break
        
        # Create a simple response based on the query
        if "grocery" in user_message.lower():
            content = "I recommend shopping at Whole Foods for organic produce."
        elif "tech" in user_message.lower():
            content = "I recommend checking Best Buy and Amazon for the latest tech products."
        elif "travel" in user_message.lower():
            content = "I recommend booking through Expedia for the best travel deals."
        else:
            content = "I can help you find the best products across different retailers."
        
        return {
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": content
                    },
                    "finish_reason": "stop"
                }
            ]
        }