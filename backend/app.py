"""
Web application for the Universal Shopping Assistant with a Manus-like UI.
"""

import os
import json
import asyncio
import threading
import time
import dotenv
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO

# Import CrewAI controller
from agents.controller import ShoppingController

# Load environment variables
dotenv.load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shopping-assistant-secret-key'
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables to store agent state
agent_logs = []
current_task = "Initializing..."
shopping_list = []
agent_status = {
    "inventory": "idle",
    "dietary": "idle",
    "budget": "idle",
    "price_comparison": "idle",
    "browser": "idle",
    "tech": "idle",
    "travel": "idle",
    "finance": "idle"
}

# CrewAI controller instance
shopping_controller = None
use_crew_ai = True  # Flag to toggle between mock agents and CrewAI

# Function to initialize CrewAI controller
async def initialize_controller():
    global shopping_controller
    
    # Get API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Create controller
    shopping_controller = ShoppingController(
        llm_model="gpt-4o",
        api_key=api_key,
        debug=True
    )
    
    # Start the controller
    await shopping_controller.start()
    
    return shopping_controller

# Initialize controller in a separate thread
def init_controller_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(initialize_controller())

# Run the agent in a separate thread
def run_agent_task(query):
    global agent_logs, current_task, shopping_list, agent_status
    
    # Reset agent state
    agent_logs = []
    current_task = "Processing query: " + query
    shopping_list = []
    
    # Update agent status
    agent_status = {key: "initializing" for key in agent_status}
    socketio.emit('agent_status', agent_status)
    
    # Log initialization
    log_entry = {
        "timestamp": time.time(),
        "type": "info",
        "message": f"Initializing assistant with query: {query}"
    }
    agent_logs.append(log_entry)
    socketio.emit('agent_log', log_entry)
    
    try:
        # Run with CrewAI if enabled
        if use_crew_ai and shopping_controller:
            # Create event loop for async operation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Prepare user preferences
            user_preferences = {
                "user_query": query
            }
            
            # Process query with controller
            result = loop.run_until_complete(shopping_controller.process_query(user_preferences))
            
            # Get shopping list from result
            if "shopping_list" in result:
                shopping_list = result["shopping_list"]
            
            # Log success
            log_entry = {
                "timestamp": time.time(),
                "type": "success",
                "message": f"Successfully processed query: {query}"
            }
            agent_logs.append(log_entry)
            socketio.emit('agent_log', log_entry)
        else:
            # Mock implementation for testing
            # This simulates the agent behavior without CrewAI
            mock_processing(query)
    except Exception as e:
        # Log error
        log_entry = {
            "timestamp": time.time(),
            "type": "error",
            "message": f"Error: {str(e)}"
        }
        agent_logs.append(log_entry)
        socketio.emit('agent_log', log_entry)
    
    # Reset agent status to idle
    agent_status = {key: "idle" for key in agent_status}
    socketio.emit('agent_status', agent_status)
    
    # Set current task to completed
    current_task = "Completed"
    socketio.emit('current_task', current_task)

def mock_processing(query):
    """Mock implementation for testing without CrewAI."""
    global agent_logs, current_task, shopping_list, agent_status
    
    # Log initialization
    log_entry = {
        "timestamp": time.time(),
        "type": "info",
        "message": f"[MOCK] Processing query: {query}"
    }
    agent_logs.append(log_entry)
    socketio.emit('agent_log', log_entry)
    
    # Determine query type
    if any(kw in query.lower() for kw in ["tech", "laptop", "phone", "computer", "gadget"]):
        query_type = "tech"
    elif any(kw in query.lower() for kw in ["travel", "vacation", "hotel", "flight"]):
        query_type = "travel"
    elif any(kw in query.lower() for kw in ["invest", "finance", "stock", "etf", "fund"]):
        query_type = "finance"
    else:
        query_type = "grocery"
    
    log_entry = {
        "timestamp": time.time(),
        "type": "info",
        "message": f"[MOCK] Detected query type: {query_type}"
    }
    agent_logs.append(log_entry)
    socketio.emit('agent_log', log_entry)
    
    # Update agent status based on query type
    if query_type == "grocery":
        # Simulate inventory agent
        agent_status["inventory"] = "active"
        socketio.emit('agent_status', agent_status)
        time.sleep(1)
        
        log_entry = {
            "timestamp": time.time(),
            "type": "info",
            "message": "[MOCK] Inventory Agent: Analyzing current household inventory"
        }
        agent_logs.append(log_entry)
        socketio.emit('agent_log', log_entry)
        
        # Simulate dietary agent
        agent_status["inventory"] = "idle"
        agent_status["dietary"] = "active"
        socketio.emit('agent_status', agent_status)
        time.sleep(1)
        
        log_entry = {
            "timestamp": time.time(),
            "type": "info",
            "message": "[MOCK] Dietary Agent: Filtering items based on dietary preferences"
        }
        agent_logs.append(log_entry)
        socketio.emit('agent_log', log_entry)
        
        # Simulate budget agent
        agent_status["dietary"] = "idle"
        agent_status["budget"] = "active"
        socketio.emit('agent_status', agent_status)
        time.sleep(1)
        
        log_entry = {
            "timestamp": time.time(),
            "type": "info",
            "message": "[MOCK] Budget Agent: Optimizing shopping list based on budget constraints"
        }
        agent_logs.append(log_entry)
        socketio.emit('agent_log', log_entry)
        
        # Simulate price comparison agent
        agent_status["budget"] = "idle"
        agent_status["price_comparison"] = "active"
        socketio.emit('agent_status', agent_status)
        time.sleep(1)
        
        log_entry = {
            "timestamp": time.time(),
            "type": "info",
            "message": "[MOCK] Price Comparison Agent: Finding the best prices across stores"
        }
        agent_logs.append(log_entry)
        socketio.emit('agent_log', log_entry)
        
        # Simulate browser agent
        agent_status["price_comparison"] = "idle"
        agent_status["browser"] = "active"
        socketio.emit('agent_status', agent_status)
        
        # Simulate visiting different stores
        stores = ["Walmart", "Target", "Kroger", "Whole Foods", "Amazon Fresh"]
        for store in stores:
            log_entry = {
                "timestamp": time.time(),
                "type": "info",
                "message": f"[MOCK] Browser Agent: Visiting {store} to find the best deals"
            }
            agent_logs.append(log_entry)
            socketio.emit('agent_log', log_entry)
            
            # Simulate browser activity
            socketio.emit('browser_activity', {
                "type": "navigation",
                "url": f"https://www.{store.lower().replace(' ', '')}.com/search?q={query.replace(' ', '+')}"
            })
            
            time.sleep(1)
        
        # Generate mock shopping list
        shopping_list = [
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
    
    elif query_type == "tech":
        # Simulate tech product agent
        agent_status["tech"] = "active"
        socketio.emit('agent_status', agent_status)
        
        # Simulate browser agent
        agent_status["browser"] = "active"
        socketio.emit('agent_status', agent_status)
        
        # Simulate visiting different tech stores
        tech_stores = ["BestBuy", "Amazon", "Newegg", "MicroCenter", "B&H"]
        for store in tech_stores:
            log_entry = {
                "timestamp": time.time(),
                "type": "info",
                "message": f"[MOCK] Browser Agent: Visiting {store} to research tech products"
            }
            agent_logs.append(log_entry)
            socketio.emit('agent_log', log_entry)
            
            # Simulate browser activity
            socketio.emit('browser_activity', {
                "type": "navigation",
                "url": f"https://www.{store.lower().replace(' ', '').replace('&', '')}.com/search?q={query.replace(' ', '+')}"
            })
            
            time.sleep(1)
        
        # Generate mock tech shopping list
        if "laptop" in query.lower():
            shopping_list = [
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
            shopping_list = [
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
    
    elif query_type == "travel":
        # Simulate travel agent
        agent_status["travel"] = "active"
        socketio.emit('agent_status', agent_status)
        
        # Simulate browser agent
        agent_status["browser"] = "active"
        socketio.emit('agent_status', agent_status)
        
        # Simulate visiting different travel sites
        travel_sites = ["Expedia", "Booking.com", "Kayak", "Airbnb", "Hotels.com"]
        for site in travel_sites:
            log_entry = {
                "timestamp": time.time(),
                "type": "info",
                "message": f"[MOCK] Browser Agent: Visiting {site} to research travel options"
            }
            agent_logs.append(log_entry)
            socketio.emit('agent_log', log_entry)
            
            # Simulate browser activity
            socketio.emit('browser_activity', {
                "type": "navigation",
                "url": f"https://www.{site.lower().replace(' ', '').replace('.', '')}.com/search?q={query.replace(' ', '+')}"
            })
            
            time.sleep(1)
        
        # Generate mock travel options
        shopping_list = [
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
    
    elif query_type == "finance":
        # Simulate finance agent
        agent_status["finance"] = "active"
        socketio.emit('agent_status', agent_status)
        
        # Simulate browser agent
        agent_status["browser"] = "active"
        socketio.emit('agent_status', agent_status)
        
        # Simulate visiting different finance sites
        finance_sites = ["Vanguard", "Fidelity", "Charles Schwab", "Robinhood", "E*TRADE"]
        for site in finance_sites:
            log_entry = {
                "timestamp": time.time(),
                "type": "info",
                "message": f"[MOCK] Browser Agent: Visiting {site} to research investment options"
            }
            agent_logs.append(log_entry)
            socketio.emit('agent_log', log_entry)
            
            # Simulate browser activity
            socketio.emit('browser_activity', {
                "type": "navigation",
                "url": f"https://www.{site.lower().replace(' ', '').replace('*', '').replace('&', '')}.com/search?q={query.replace(' ', '+')}"
            })
            
            time.sleep(1)
        
        # Generate mock investment options
        shopping_list = [
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
    
    # Log completion
    log_entry = {
        "timestamp": time.time(),
        "type": "success",
        "message": f"[MOCK] Successfully processed query: {query}"
    }
    agent_logs.append(log_entry)
    socketio.emit('agent_log', log_entry)

# API Routes
@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok"})

@app.route('/api/run', methods=['POST'])
def run_agent():
    """Run the agent with the specified query."""
    data = request.json
    user_query = data.get('query', '')
    
    # Start the agent in a separate thread
    thread = threading.Thread(target=run_agent_task, args=(user_query,))
    thread.daemon = True
    thread.start()
    
    return jsonify({"status": "started"})

@app.route('/api/status')
def get_status():
    """Get the current status of the agent."""
    return jsonify({
        "current_task": current_task,
        "agent_status": agent_status
    })

@app.route('/api/logs')
def get_logs():
    """Get the agent logs."""
    return jsonify(agent_logs)

@app.route('/api/shopping/list')
def api_shopping_list():
    """Get the shopping list."""
    return jsonify(shopping_list)

@app.route('/api/agent/stop', methods=['POST'])
def api_stop_agent():
    """Stop the agent."""
    global current_task
    current_task = "Stopped by user"
    
    # Stop controller if using it
    if use_crew_ai and shopping_controller:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(shopping_controller.stop())
    
    return jsonify({"status": "stopped"})

@app.route('/api/agent/status')
def api_agent_status():
    """Get the status of the agent."""
    return jsonify({
        "is_running": current_task != "Initializing..." and current_task != "Completed" and current_task != "Stopped by user",
        "current_task": current_task,
        "agent_status": agent_status
    })

@app.route('/api/agent/toggle-crew', methods=['POST'])
def api_toggle_crew():
    """Toggle between mock agents and CrewAI."""
    global use_crew_ai
    
    data = request.json
    use_crew_ai = data.get('useCrewAI', True)
    
    # Initialize controller if needed
    if use_crew_ai and shopping_controller is None:
        init_thread = threading.Thread(target=init_controller_thread)
        init_thread.daemon = True
        init_thread.start()
    
    return jsonify({"status": "success", "useCrewAI": use_crew_ai})

# Enable CORS for Socket.IO
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Initialize controller when app starts
if __name__ == '__main__':
    # Initialize controller in a separate thread
    if use_crew_ai:
        init_thread = threading.Thread(target=init_controller_thread)
        init_thread.daemon = True
        init_thread.start()
    
    # Start the Socket.IO server
    socketio.run(app, debug=True, use_reloader=True)