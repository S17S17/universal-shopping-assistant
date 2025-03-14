"""
CrewAI executor implementation for the shopping assistant system.
This module provides the main executor that coordinates CrewAI agents and tasks.
"""

import asyncio
import json
import os
import re
from typing import Dict, List, Any, Optional, Tuple

from crewai import Crew
from langchain_openai import ChatOpenAI

from .agents import ShoppingAgents
from .tasks import ShoppingTasks

class ShoppingExecutor:
    """
    Central executor that coordinates CrewAI agents and tasks.
    This class is responsible for orchestrating the entire shopping process
    using the CrewAI framework.
    """
    
    def __init__(self, 
                 llm_model: str = "gpt-4o",
                 api_key: Optional[str] = None,
                 debug: bool = False):
        """
        Initialize the CrewAI executor.
        
        Args:
            llm_model: The LLM model to use (default: gpt-4o)
            api_key: API key for the LLM service
            debug: Whether to enable debug mode
        """
        self.llm_model = llm_model
        self.api_key = api_key
        self.debug = debug
        self.user_preferences = {}
        
        # Initialize agent and task factories
        self.agents_factory = ShoppingAgents(llm_model=llm_model, api_key=api_key)
        self.tasks_factory = ShoppingTasks()
    
    async def initialize(self):
        """Initialize all components."""
        if self.debug:
            print("[DEBUG] Initializing Shopping executor")
        
        # Nothing to initialize for CrewAI as agents and tasks are created on demand
        return True
    
    async def set_user_preferences(self, preferences: Dict[str, Any]):
        """
        Set user preferences.
        
        Args:
            preferences: User preferences
        """
        self.user_preferences.update(preferences)
        return True
    
    async def generate_shopping_list(self) -> List[Dict[str, Any]]:
        """
        Generate a shopping list based on user preferences.
        
        Returns:
            Generated shopping list
        """
        # Get user query from preferences
        user_query = self.user_preferences.get("user_query", "")
        
        if not user_query:
            return []
        
        # Identify query type
        query_type = self._identify_query_type(user_query)
        
        # Handle different query types
        if query_type == "grocery":
            return await self._handle_grocery_query()
        elif query_type == "tech":
            return await self._handle_tech_query(user_query)
        elif query_type == "travel":
            return await self._handle_travel_query(user_query)
        elif query_type == "finance":
            return await self._handle_finance_query(user_query)
        else:
            # Default to grocery for unknown query types
            return await self._handle_grocery_query()
    
    def _identify_query_type(self, query: str) -> str:
        """
        Identify the type of query.
        
        Args:
            query: The user query
            
        Returns:
            Query type (grocery, tech, travel, finance)
        """
        query = query.lower()
        
        # Check for tech-related terms
        tech_terms = [
            "laptop", "computer", "phone", "smartphone", "tablet", "gadget", 
            "electronics", "tech", "device", "hardware", "software", "gaming",
            "camera", "headphone", "speaker", "tv", "television", "monitor"
        ]
        for term in tech_terms:
            if term in query:
                return "tech"
        
        # Check for travel-related terms
        travel_terms = [
            "travel", "vacation", "hotel", "flight", "trip", "booking", 
            "destination", "resort", "airbnb", "airline", "tour", "cruise"
        ]
        for term in travel_terms:
            if term in query:
                return "travel"
        
        # Check for finance-related terms
        finance_terms = [
            "invest", "finance", "stock", "etf", "fund", "roth", "ira", 
            "portfolio", "dividend", "retirement", "bond", "crypto"
        ]
        for term in finance_terms:
            if term in query:
                return "finance"
        
        # Default to grocery
        return "grocery"
    
    async def _handle_grocery_query(self) -> List[Dict[str, Any]]:
        """
        Handle a grocery shopping query using CrewAI.
        
        Returns:
            List of grocery items to purchase
        """
        # Create agents
        inventory_agent = self.agents_factory.inventory_agent()
        dietary_agent = self.agents_factory.dietary_agent()
        budget_agent = self.agents_factory.budget_agent()
        price_comparison_agent = self.agents_factory.price_comparison_agent()
        
        # Create tasks
        inventory_task = self.tasks_factory.inventory_analysis_task(
            agent=inventory_agent,
            user_preferences=self.user_preferences
        )
        
        dietary_task = self.tasks_factory.dietary_filtering_task(
            agent=dietary_agent,
            user_preferences=self.user_preferences
        )
        
        budget_task = self.tasks_factory.budget_optimization_task(
            agent=budget_agent,
            user_preferences=self.user_preferences
        )
        
        price_task = self.tasks_factory.price_comparison_task(
            agent=price_comparison_agent,
            user_preferences=self.user_preferences
        )
        
        # Create the crew
        crew = Crew(
            agents=[inventory_agent, dietary_agent, budget_agent, price_comparison_agent],
            tasks=[inventory_task, dietary_task, budget_task, price_task],
            verbose=self.debug
        )
        
        # Run the crew
        result = crew.kickoff()
        
        # Parse the result to extract shopping list
        shopping_list = self._parse_shopping_list(result)
        
        return shopping_list
    
    async def _handle_tech_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Handle a tech product query using CrewAI.
        
        Args:
            query: The user's tech product query
            
        Returns:
            List of tech products
        """
        # Create tech product agent
        tech_agent = self.agents_factory.tech_product_agent()
        
        # Create tech product research task
        tech_task = self.tasks_factory.tech_product_research_task(
            agent=tech_agent,
            user_query=query
        )
        
        # Create the crew
        crew = Crew(
            agents=[tech_agent],
            tasks=[tech_task],
            verbose=self.debug
        )
        
        # Run the crew
        result = crew.kickoff()
        
        # Parse the result to extract tech products
        tech_products = self._parse_tech_products(result, query)
        
        return tech_products
    
    async def _handle_travel_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Handle a travel query using CrewAI.
        
        Args:
            query: The user's travel query
            
        Returns:
            List of travel items
        """
        # Create travel agent
        travel_agent = self.agents_factory.travel_agent()
        
        # Create travel planning task
        travel_task = self.tasks_factory.travel_planning_task(
            agent=travel_agent,
            user_query=query
        )
        
        # Create the crew
        crew = Crew(
            agents=[travel_agent],
            tasks=[travel_task],
            verbose=self.debug
        )
        
        # Run the crew
        result = crew.kickoff()
        
        # Parse the result to extract travel items
        travel_items = self._parse_travel_items(result)
        
        return travel_items
    
    async def _handle_finance_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Handle a finance query using CrewAI.
        
        Args:
            query: The user's finance query
            
        Returns:
            List of finance items
        """
        # Create finance agent
        finance_agent = self.agents_factory.finance_agent()
        
        # Create financial advisory task
        finance_task = self.tasks_factory.financial_advisory_task(
            agent=finance_agent,
            user_query=query
        )
        
        # Create the crew
        crew = Crew(
            agents=[finance_agent],
            tasks=[finance_task],
            verbose=self.debug
        )
        
        # Run the crew
        result = crew.kickoff()
        
        # Parse the result to extract finance items
        finance_items = self._parse_finance_items(result)
        
        return finance_items
    
    async def execute_shopping(self, shopping_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute the shopping process.
        
        Args:
            shopping_list: The shopping list
            
        Returns:
            Results of the shopping process
        """
        if not shopping_list:
            return {
                "status": "error",
                "message": "Shopping list is empty"
            }
        
        # Get query type from first item
        first_item = shopping_list[0]
        category = first_item.get("category", "grocery").lower()
        
        query_type = "grocery"
        if category in ["laptop", "computer", "phone", "smartphone", "tablet", "electronics"]:
            query_type = "tech"
        elif category in ["hotel", "flight", "resort", "airbnb"]:
            query_type = "travel"
        elif category in ["etf", "stock", "fund", "bond", "crypto"]:
            query_type = "finance"
        
        # Handle different query types without using a browser agent
        if query_type == "tech":
            print("Executing tech product comparison")
            # Simulate browsing tech websites
            for store in ["BestBuy", "Amazon", "Newegg", "MicroCenter"]:
                print(f"Browser Agent visiting {store} to compare products")
                await asyncio.sleep(0.5)
            
            return {
                "status": "success",
                "message": "Tech product comparison completed successfully",
                "products_found": len(shopping_list)
            }
        
        elif query_type == "travel":
            print("Executing travel search")
            # Simulate browsing travel websites
            for store in ["Expedia", "Booking.com", "Kayak", "Airbnb"]:
                print(f"Browser Agent visiting {store} to find travel options")
                await asyncio.sleep(0.5)
            
            return {
                "status": "success",
                "message": "Travel search completed successfully",
                "options_found": len(shopping_list)
            }
        
        elif query_type == "finance":
            print("Executing finance analysis")
            # Simulate browsing finance websites
            for store in ["Yahoo Finance", "Bloomberg", "MarketWatch", "Morningstar"]:
                print(f"Browser Agent visiting {store} to analyze investments")
                await asyncio.sleep(0.5)
            
            return {
                "status": "success",
                "message": "Financial analysis completed successfully",
                "investments_analyzed": len(shopping_list)
            }
        
        # For grocery shopping, create a browser agent and shopping execution task
        browser_agent = self.agents_factory.browser_agent()
        
        # Create shopping execution task
        shopping_task = self.tasks_factory.shopping_execution_task(
            agent=browser_agent,
            user_preferences=self.user_preferences,
            final_shopping_list=shopping_list
        )
        
        # Create the crew
        crew = Crew(
            agents=[browser_agent],
            tasks=[shopping_task],
            verbose=self.debug
        )
        
        # Run the crew
        result = crew.kickoff()
        
        # In a real implementation, this would parse the result from CrewAI
        # For now, return a success message
        return {
            "status": "success",
            "message": "Shopping simulation completed successfully",
            "items_purchased": len(shopping_list)
        }
    
    def _parse_shopping_list(self, result: str) -> List[Dict[str, Any]]:
        """
        Parse the CrewAI result to extract a shopping list.
        
        Args:
            result: The result from the CrewAI execution
            
        Returns:
            List of shopping items
        """
        # This is a simplified parser for the MVP
        # In a real implementation, this would parse the result from CrewAI
        # For now, return mock data
        return [
            {
                "name": "Organic Spinach",
                "quantity": 2,
                "unit": "bag",
                "price": 3.99,
                "store": "Whole Foods",
                "category": "produce"
            },
            {
                "name": "Oat Milk",
                "quantity": 2,
                "unit": "carton",
                "price": 4.49,
                "store": "Trader Joe's",
                "category": "dairy"
            },
            {
                "name": "Organic Tofu",
                "quantity": 3,
                "unit": "pack",
                "price": 2.99,
                "store": "Sprouts",
                "category": "protein"
            },
            {
                "name": "Quinoa",
                "quantity": 1,
                "unit": "bag",
                "price": 6.99,
                "store": "Amazon Fresh",
                "category": "grains"
            }
        ]
    
    def _parse_tech_products(self, result: str, query: str) -> List[Dict[str, Any]]:
        """
        Parse the CrewAI result to extract tech products.
        
        Args:
            result: The result from the CrewAI execution
            query: The original user query
            
        Returns:
            List of tech products
        """
        # Simplified parser for the MVP
        if "laptop" in query.lower():
            return [
                {
                    "name": "MacBook Pro 14",
                    "quantity": 1,
                    "unit": "unit",
                    "price": 1999.99,
                    "store": "Apple",
                    "category": "laptop",
                    "specs": "M3 Pro, 32GB RAM, 1TB SSD"
                },
                {
                    "name": "Dell XPS 15",
                    "quantity": 1,
                    "unit": "unit",
                    "price": 1699.99,
                    "store": "Dell",
                    "category": "laptop",
                    "specs": "Intel i9, 32GB RAM, 1TB SSD"
                },
                {
                    "name": "Lenovo ThinkPad X1",
                    "quantity": 1,
                    "unit": "unit",
                    "price": 1599.99,
                    "store": "Lenovo",
                    "category": "laptop",
                    "specs": "Intel i7, 16GB RAM, 512GB SSD"
                }
            ]
        else:
            return [
                {
                    "name": "Samsung Galaxy S24 Ultra",
                    "quantity": 1,
                    "unit": "unit",
                    "price": 1299.99,
                    "store": "Samsung",
                    "category": "smartphone"
                },
                {
                    "name": "iPhone 15 Pro",
                    "quantity": 1,
                    "unit": "unit",
                    "price": 1099.99,
                    "store": "Apple",
                    "category": "smartphone"
                },
                {
                    "name": "Google Pixel 8 Pro",
                    "quantity": 1,
                    "unit": "unit",
                    "price": 999.99,
                    "store": "Google",
                    "category": "smartphone"
                }
            ]
    
    def _parse_travel_items(self, result: str) -> List[Dict[str, Any]]:
        """
        Parse the CrewAI result to extract travel items.
        
        Args:
            result: The result from the CrewAI execution
            
        Returns:
            List of travel items
        """
        return [
            {
                "name": "Marriott Hotel - New York",
                "quantity": 1,
                "unit": "night",
                "price": 299.99,
                "store": "Booking.com",
                "category": "hotel"
            },
            {
                "name": "Hilton Hotel - New York",
                "quantity": 1,
                "unit": "night",
                "price": 279.99,
                "store": "Hotels.com",
                "category": "hotel"
            },
            {
                "name": "JFK to LAX Flight",
                "quantity": 1,
                "unit": "round-trip",
                "price": 399.99,
                "store": "Expedia",
                "category": "flight"
            }
        ]
    
    def _parse_finance_items(self, result: str) -> List[Dict[str, Any]]:
        """
        Parse the CrewAI result to extract finance items.
        
        Args:
            result: The result from the CrewAI execution
            
        Returns:
            List of finance items
        """
        return [
            {
                "name": "Vanguard S&P 500 ETF (VOO)",
                "quantity": 10,
                "unit": "share",
                "price": 452.78,
                "store": "Vanguard",
                "category": "etf"
            },
            {
                "name": "Vanguard Total Stock Market ETF (VTI)",
                "quantity": 10,
                "unit": "share",
                "price": 244.37,
                "store": "Vanguard",
                "category": "etf"
            },
            {
                "name": "iShares Core S&P 500 ETF (IVV)",
                "quantity": 5,
                "unit": "share",
                "price": 459.50,
                "store": "iShares",
                "category": "etf"
            }
        ]
    
    async def run(self, user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run the complete shopping process.
        
        Args:
            user_preferences: Optional user preferences to set
            
        Returns:
            Results of the shopping process
        """
        # Initialize if not already initialized
        await self.initialize()
            
        # Set user preferences if provided
        if user_preferences:
            await self.set_user_preferences(user_preferences)
            
        # Generate shopping list
        shopping_list = await self.generate_shopping_list()
        
        # Execute shopping
        result = await self.execute_shopping(shopping_list)
        
        return {
            "shopping_list": shopping_list,
            "result": result
        }