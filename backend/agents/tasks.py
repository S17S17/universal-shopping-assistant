"""
CrewAI tasks implementation for the shopping assistant system.
This module defines the specialized tasks used in the CrewAI-based system.
"""

from crewai import Task
from typing import Dict, Any, List, Optional
from textwrap import dedent

class ShoppingTasks:
    """
    Factory class for creating specialized CrewAI tasks for shopping assistant.
    """
    
    def inventory_analysis_task(self, agent, user_preferences: Dict[str, Any]) -> Task:
        """
        Create a task for analyzing current inventory and determining needed items.
        
        Args:
            agent: The agent to assign this task to
            user_preferences: User preferences including inventory information
            
        Returns:
            A CrewAI Task
        """
        inventory_data = user_preferences.get('inventory', {})
        inventory_items = inventory_data.get('current_items', [])
        inventory_str = "\n".join([f"- {item.get('name', 'Unknown')}: {item.get('quantity', 0)} {item.get('unit', '')}" 
                                 for item in inventory_items])
        
        user_query = user_preferences.get('user_query', 'Generate a shopping list')
        
        return Task(
            description=dedent(f"""
                Analyze the current inventory and determine what items need to be purchased.
                Consider standard household items that might be running low based on typical usage patterns.
                Consider the user's query: "{user_query}"
                
                Current inventory:
                {inventory_str if inventory_str else "No inventory data provided."}
                
                Your final answer should be a list of items that need to be purchased, with quantities.
            """),
            agent=agent,
            expected_output="A list of items that need to be purchased with quantities"
        )
    
    def dietary_filtering_task(self, agent, user_preferences: Dict[str, Any]) -> Task:
        """
        Create a task for filtering items based on dietary preferences.
        
        Args:
            agent: The agent to assign this task to
            user_preferences: User preferences including dietary information
            
        Returns:
            A CrewAI Task
        """
        dietary_data = user_preferences.get('dietary', {})
        restrictions = dietary_data.get('restrictions', [])
        preferences = dietary_data.get('preferences', [])
        
        restrictions_str = ", ".join(restrictions) if restrictions else "None"
        preferences_str = ", ".join(preferences) if preferences else "None"
        
        user_query = user_preferences.get('user_query', 'Filter items based on dietary preferences')
        
        return Task(
            description=dedent(f"""
                Filter food items based on dietary preferences and restrictions.
                Consider the user's query: "{user_query}"
                
                Dietary restrictions: {restrictions_str}
                Dietary preferences: {preferences_str}
                
                Your final answer should be a list of items that meet the dietary criteria.
            """),
            agent=agent,
            expected_output="A list of items that meet the dietary criteria"
        )
    
    def budget_optimization_task(self, agent, user_preferences: Dict[str, Any]) -> Task:
        """
        Create a task for optimizing shopping list based on budget constraints.
        
        Args:
            agent: The agent to assign this task to
            user_preferences: User preferences including budget information
            
        Returns:
            A CrewAI Task
        """
        budget_data = user_preferences.get('budget', {})
        max_budget = budget_data.get('max_budget', 0)
        
        user_query = user_preferences.get('user_query', 'Optimize shopping list based on budget')
        
        return Task(
            description=dedent(f"""
                Optimize the shopping list based on budget constraints.
                Consider the user's query: "{user_query}"
                
                Maximum budget: ${max_budget if max_budget else 'Not specified'}
                
                Your final answer should be an optimized shopping list that stays within budget.
            """),
            agent=agent,
            expected_output="An optimized shopping list within budget constraints"
        )
    
    def price_comparison_task(self, agent, user_preferences: Dict[str, Any]) -> Task:
        """
        Create a task for comparing prices across different stores.
        
        Args:
            agent: The agent to assign this task to
            user_preferences: User preferences including store information
            
        Returns:
            A CrewAI Task
        """
        store_data = user_preferences.get('stores', {})
        preferred_stores = store_data.get('preferred', [])
        
        preferred_stores_str = ", ".join(preferred_stores) if preferred_stores else "All stores"
        
        user_query = user_preferences.get('user_query', 'Compare prices across stores')
        
        return Task(
            description=dedent(f"""
                Compare prices for items across different stores.
                Consider the user's query: "{user_query}"
                
                Preferred stores: {preferred_stores_str}
                
                Your final answer should be a list of items with the best price and store information.
            """),
            agent=agent,
            expected_output="A list of items with optimal prices and store information"
        )
    
    def shopping_execution_task(self, agent, user_preferences: Dict[str, Any], final_shopping_list: List[Dict[str, Any]]) -> Task:
        """
        Create a task for executing the shopping process.
        
        Args:
            agent: The agent to assign this task to
            user_preferences: User preferences
            final_shopping_list: Final shopping list with store recommendations
            
        Returns:
            A CrewAI Task
        """
        items_by_store = {}
        for item in final_shopping_list:
            store = item.get('store', 'Unknown')
            if store not in items_by_store:
                items_by_store[store] = []
            items_by_store[store].append(item)
        
        stores_items_str = ""
        for store, items in items_by_store.items():
            items_str = "\n".join([f"  - {item.get('name', 'Unknown')}: {item.get('quantity', 0)} {item.get('unit', '')}" 
                                 for item in items])
            stores_items_str += f"{store}:\n{items_str}\n\n"
        
        user_query = user_preferences.get('user_query', 'Execute shopping process')
        
        return Task(
            description=dedent(f"""
                Execute the shopping process by visiting each store's website and adding items to the cart.
                Simulate the checkout process but stop before finalizing payment.
                Consider the user's query: "{user_query}"
                
                Shopping list by store:
                {stores_items_str if stores_items_str else "No items provided."}
                
                Your final answer should be a detailed report of the shopping process, including any issues encountered.
            """),
            agent=agent,
            expected_output="A detailed report of the shopping process"
        )
    
    def tech_product_research_task(self, agent, user_query: str) -> Task:
        """
        Create a task for researching tech products.
        
        Args:
            agent: The agent to assign this task to
            user_query: The user's tech product query
            
        Returns:
            A CrewAI Task
        """
        return Task(
            description=dedent(f"""
                Research and recommend tech products based on the user's query.
                User query: "{user_query}"
                
                1. Identify the specific tech product category the user is interested in.
                2. Research the top products in this category considering factors like:
                   - Feature specifications
                   - Price range
                   - User reviews
                   - Availability
                3. Compare the products across different retailers.
                4. Recommend the best options with justification.
                
                Your final answer should be a detailed comparison of the best tech products
                that match the user's query, with specific recommendations.
            """),
            agent=agent,
            expected_output="A detailed comparison of tech products with recommendations"
        )
    
    def travel_planning_task(self, agent, user_query: str) -> Task:
        """
        Create a task for planning travel itineraries.
        
        Args:
            agent: The agent to assign this task to
            user_query: The user's travel query
            
        Returns:
            A CrewAI Task
        """
        return Task(
            description=dedent(f"""
                Research and plan a travel itinerary based on the user's query.
                User query: "{user_query}"
                
                1. Identify the specific travel needs (destination, dates, budget, preferences).
                2. Research the best options for:
                   - Flights or transportation
                   - Accommodations
                   - Activities and attractions
                3. Compare options across different booking platforms.
                4. Create an optimal itinerary with pricing details.
                
                Your final answer should be a detailed travel plan that matches
                the user's query, with specific recommendations and pricing.
            """),
            agent=agent,
            expected_output="A detailed travel plan with recommendations and pricing"
        )
    
    def financial_advisory_task(self, agent, user_query: str) -> Task:
        """
        Create a task for providing financial advice.
        
        Args:
            agent: The agent to assign this task to
            user_query: The user's finance query
            
        Returns:
            A CrewAI Task
        """
        return Task(
            description=dedent(f"""
                Research and provide financial recommendations based on the user's query.
                User query: "{user_query}"
                
                1. Identify the specific financial needs or goals.
                2. Research appropriate investment options or financial strategies.
                3. Compare options across different financial institutions.
                4. Create a recommended financial plan with justification.
                
                Your final answer should be detailed financial recommendations
                that match the user's query, with specific investment suggestions
                and expected outcomes.
            """),
            agent=agent,
            expected_output="Detailed financial recommendations with specific investment suggestions"
        )