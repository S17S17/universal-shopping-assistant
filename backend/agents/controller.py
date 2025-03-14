"""
Controller for the CrewAI-based shopping assistant system.
This module provides a controller that integrates the CrewAI implementation
with the existing application.
"""

import asyncio
import json
import os
from typing import Dict, List, Any, Optional

from .executor import ShoppingExecutor

class ShoppingController:
    """
    Controller for the CrewAI-based shopping assistant system.
    This class provides methods to interact with the CrewAI implementation
    and integrate it with the existing application.
    """
    
    def __init__(self, 
                 llm_model: str = "gpt-4o",
                 api_key: Optional[str] = None,
                 debug: bool = False):
        """
        Initialize the controller.
        
        Args:
            llm_model: The LLM model to use (default: gpt-4o)
            api_key: API key for the LLM service
            debug: Whether to enable debug mode
        """
        self.executor = ShoppingExecutor(llm_model=llm_model, api_key=api_key, debug=debug)
        self.debug = debug
        self.is_running = False
        self.current_task = None
        self.shopping_list = []
        self.shopping_result = {}
    
    async def start(self):
        """Start the controller."""
        if self.debug:
            print("[DEBUG] Starting CrewAI controller")
        
        # Initialize the executor
        await self.executor.initialize()
        self.is_running = True
        
        return {"status": "success", "message": "Shopping controller started successfully"}
    
    async def stop(self):
        """Stop the controller."""
        if self.debug:
            print("[DEBUG] Stopping CrewAI controller")
        
        self.is_running = False
        self.current_task = None
        
        return {"status": "success", "message": "Shopping controller stopped successfully"}
    
    async def status(self):
        """Get the status of the controller."""
        return {
            "is_running": self.is_running,
            "current_task": self.current_task,
            "has_shopping_list": len(self.shopping_list) > 0,
            "items_count": len(self.shopping_list)
        }
    
    async def process_query(self, preferences: Dict[str, Any] = None):
        """
        Process a user query.
        
        Args:
            preferences: User preferences including the query
            
        Returns:
            Results of the query processing
        """
        if not self.is_running:
            return {"status": "error", "message": "Controller is not running"}
        
        # Set current task
        self.current_task = "processing_query"
        
        # Prepare user preferences
        user_preferences = preferences or {}
        
        # Make sure query is present
        if "user_query" not in user_preferences:
            return {"status": "error", "message": "Missing user query in preferences"}
        
        try:
            # Run the executor
            self.current_task = "running_executor"
            result = await self.executor.run(user_preferences)
            
            # Store the shopping list and result
            self.shopping_list = result.get("shopping_list", [])
            self.shopping_result = result.get("result", {})
            
            # Set current task to None
            self.current_task = None
            
            return {
                "status": "success",
                "message": "Query processed successfully",
                "shopping_list": self.shopping_list,
                "result": self.shopping_result
            }
        except Exception as e:
            self.current_task = None
            return {"status": "error", "message": f"Error processing query: {str(e)}"}
    
    async def get_shopping_list(self):
        """
        Get the current shopping list.
        
        Returns:
            The current shopping list
        """
        return self.shopping_list
    
    async def get_shopping_result(self):
        """
        Get the result of the shopping process.
        
        Returns:
            The result of the shopping process
        """
        return self.shopping_result
    
    async def execute_shopping(self, shopping_list: List[Dict[str, Any]] = None):
        """
        Execute the shopping process.
        
        Args:
            shopping_list: Optional shopping list to use
            
        Returns:
            Results of the shopping process
        """
        if not self.is_running:
            return {"status": "error", "message": "Controller is not running"}
        
        # Set current task
        self.current_task = "executing_shopping"
        
        try:
            # Use the provided shopping list or the current one
            shopping_list = shopping_list or self.shopping_list
            
            # Execute shopping
            result = await self.executor.execute_shopping(shopping_list)
            
            # Store the result
            self.shopping_result = result
            
            # Set current task to None
            self.current_task = None
            
            return {
                "status": "success",
                "message": "Shopping executed successfully",
                "result": result
            }
        except Exception as e:
            self.current_task = None
            return {"status": "error", "message": f"Error executing shopping: {str(e)}"}
    
    async def set_preferences(self, preferences: Dict[str, Any]):
        """
        Set user preferences.
        
        Args:
            preferences: User preferences
            
        Returns:
            Status of the operation
        """
        if not self.is_running:
            return {"status": "error", "message": "Controller is not running"}
        
        # Set current task
        self.current_task = "setting_preferences"
        
        try:
            # Set preferences
            await self.executor.set_user_preferences(preferences)
            
            # Set current task to None
            self.current_task = None
            
            return {
                "status": "success",
                "message": "Preferences set successfully"
            }
        except Exception as e:
            self.current_task = None
            return {"status": "error", "message": f"Error setting preferences: {str(e)}"}
    
    async def generate_shopping_list(self):
        """
        Generate a shopping list based on user preferences.
        
        Returns:
            The generated shopping list
        """
        if not self.is_running:
            return {"status": "error", "message": "Controller is not running"}
        
        # Set current task
        self.current_task = "generating_shopping_list"
        
        try:
            # Generate shopping list
            shopping_list = await self.executor.generate_shopping_list()
            
            # Store the shopping list
            self.shopping_list = shopping_list
            
            # Set current task to None
            self.current_task = None
            
            return {
                "status": "success",
                "message": "Shopping list generated successfully",
                "shopping_list": shopping_list
            }
        except Exception as e:
            self.current_task = None
            return {"status": "error", "message": f"Error generating shopping list: {str(e)}"}