"""
CrewAI agents implementation for the shopping assistant system.
This module defines the specialized agents used in the CrewAI-based system.
"""

from crewai import Agent
# Use our local implementation instead of langchain_openai
from .chat_model import ChatOpenAI
from typing import Dict, Any, Optional

class ShoppingAgents:
    """
    Factory class for creating specialized CrewAI agents for shopping assistant.
    """
    
    def __init__(self, llm_model: str = "gpt-4o", api_key: Optional[str] = None):
        """
        Initialize the agent factory.
        
        Args:
            llm_model: The LLM model to use (default: gpt-4o)
            api_key: API key for the LLM service
        """
        self.llm_model = llm_model
        self.api_key = api_key
        self.llm = ChatOpenAI(model=llm_model, api_key=api_key)
    
    def inventory_agent(self) -> Agent:
        """Create an inventory management agent."""
        return Agent(
            role="Inventory Manager",
            goal="Track and manage household inventory to determine what items need to be purchased",
            backstory="""You are an expert inventory manager with years of experience
            in grocery and household item management. You have a keen eye for detail
            and can efficiently track what items are running low and need to be restocked.""",
            verbose=True,
            llm=self.llm
        )
    
    def dietary_agent(self) -> Agent:
        """Create a dietary preferences agent."""
        return Agent(
            role="Dietary Specialist",
            goal="Ensure all food items meet the user's dietary preferences and restrictions",
            backstory="""You are a certified nutritionist and dietary specialist with
            extensive knowledge of various diets, allergies, and food restrictions.
            You help people find food items that match their specific dietary needs
            while ensuring nutritional balance.""",
            verbose=True,
            llm=self.llm
        )
    
    def budget_agent(self) -> Agent:
        """Create a budget management agent."""
        return Agent(
            role="Budget Optimizer",
            goal="Optimize shopping lists to stay within budget while maximizing value",
            backstory="""You are a financial advisor specialized in household budgeting.
            You have helped thousands of families optimize their grocery spending
            to get the most value while staying within their budget constraints.""",
            verbose=True,
            llm=self.llm
        )
    
    def price_comparison_agent(self) -> Agent:
        """Create a price comparison agent."""
        return Agent(
            role="Price Comparison Expert",
            goal="Find the best prices for items across different stores",
            backstory="""You are a savvy shopper with an encyclopedic knowledge of
            pricing across different grocery stores and online retailers. You can
            quickly identify where to get the best deals for any product.""",
            verbose=True,
            llm=self.llm
        )
    
    def browser_agent(self) -> Agent:
        """Create a web browsing agent."""
        return Agent(
            role="Shopping Browser",
            goal="Navigate online stores to find and purchase items",
            backstory="""You are an expert in online shopping and web navigation.
            You can efficiently browse online stores, find specific items,
            compare options, and complete the checkout process.""",
            verbose=True,
            llm=self.llm
        )
    
    def tech_product_agent(self) -> Agent:
        """Create a tech product specialist agent."""
        return Agent(
            role="Tech Product Specialist",
            goal="Research and recommend the best tech products based on user requirements",
            backstory="""You are a technology expert with deep knowledge of computers,
            laptops, smartphones, and other electronic devices. You stay up-to-date with
            the latest product releases and can provide detailed comparisons and recommendations.""",
            verbose=True,
            llm=self.llm
        )
    
    def travel_agent(self) -> Agent:
        """Create a travel planning agent."""
        return Agent(
            role="Travel Planner",
            goal="Research and plan optimal travel itineraries based on user preferences",
            backstory="""You are an experienced travel agent who has planned trips
            for clients all over the world. You have extensive knowledge of destinations,
            accommodations, transportation options, and can create personalized travel plans.""",
            verbose=True,
            llm=self.llm
        )
    
    def finance_agent(self) -> Agent:
        """Create a financial advisor agent."""
        return Agent(
            role="Financial Advisor",
            goal="Provide investment and financial planning recommendations",
            backstory="""You are a certified financial advisor with expertise in
            investments, retirement planning, and personal finance. You help clients
            make informed decisions about their financial future.""",
            verbose=True,
            llm=self.llm
        )