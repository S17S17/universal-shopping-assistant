import React, { useState, useEffect, useRef } from 'react';
import BrowserSimulation from './BrowserSimulation';
import AgentConsole from './AgentConsole';
import ShoppingResults from './ShoppingResults';

const ShoppingAssistant = () => {
  const [query, setQuery] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [agentLogs, setAgentLogs] = useState([]);
  const [agentStatus, setAgentStatus] = useState({});
  const [currentTask, setCurrentTask] = useState('Idle');
  const [shoppingList, setShoppingList] = useState([]);
  const [browserActivity, setBrowserActivity] = useState(null);
  const [socketConnected, setSocketConnected] = useState(false);
  const socket = useRef(null);
  
  // Initialize WebSocket connection
  useEffect(() => {
    // Connect to WebSocket
    const socketUrl = process.env.REACT_APP_WEBSOCKET_URL || 'http://localhost:5000';
    socket.current = new WebSocket(`ws://${socketUrl.replace(/^https?:\/\//, '')}`);
    
    socket.current.onopen = () => {
      console.log('WebSocket connected');
      setSocketConnected(true);
    };
    
    socket.current.onclose = () => {
      console.log('WebSocket disconnected');
      setSocketConnected(false);
    };
    
    socket.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'agent_log') {
        setAgentLogs(prevLogs => [...prevLogs, data.log]);
      } else if (data.type === 'agent_status') {
        setAgentStatus(data.status);
      } else if (data.type === 'current_task') {
        setCurrentTask(data.task);
      } else if (data.type === 'shopping_list') {
        setShoppingList(data.list);
      } else if (data.type === 'browser_activity') {
        setBrowserActivity(data.activity);
      }
    };
    
    return () => {
      if (socket.current) {
        socket.current.close();
      }
    };
  }, []);
  
  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim() || isProcessing) return;
    
    setIsProcessing(true);
    setAgentLogs([]);
    setShoppingList([]);
    setBrowserActivity(null);
    setCurrentTask('Processing query...');
    
    try {
      const response = await fetch('/api/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to process query');
      }
      
      // Polling for status updates
      const statusInterval = setInterval(async () => {
        const statusResponse = await fetch('/api/status');
        const statusData = await statusResponse.json();
        
        if (statusData.current_task === 'Completed' || statusData.current_task === 'Stopped by user') {
          clearInterval(statusInterval);
          setIsProcessing(false);
          setCurrentTask(statusData.current_task);
          
          // Get shopping list
          const listResponse = await fetch('/api/shopping/list');
          const listData = await listResponse.json();
          setShoppingList(listData);
        } else {
          setCurrentTask(statusData.current_task);
          setAgentStatus(statusData.agent_status);
        }
      }, 1000);
    } catch (error) {
      console.error('Error processing query:', error);
      setIsProcessing(false);
      setCurrentTask('Error: ' + error.message);
    }
  };
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 h-[calc(100vh-10rem)]">
      {/* Left Column - Input and Agent Console */}
      <div className="md:col-span-1 flex flex-col space-y-4">
        {/* Query Input */}
        <div className="bg-white rounded-lg shadow p-4">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="query" className="block text-sm font-medium text-gray-700">
                What can I help you with today?
              </label>
              <textarea
                id="query"
                name="query"
                rows="3"
                className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="E.g., Compare gaming laptops with RTX 4070 GPU under $2000"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={isProcessing}
              />
            </div>
            <div className="flex justify-between items-center">
              <button
                type="submit"
                className={`px-4 py-2 bg-blue-600 text-white font-medium rounded-md ${
                  isProcessing ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'
                }`}
                disabled={isProcessing}
              >
                {isProcessing ? 'Processing...' : 'Send'}
              </button>
              {isProcessing && (
                <button
                  type="button"
                  className="px-4 py-2 bg-red-600 text-white font-medium rounded-md hover:bg-red-700"
                  onClick={async () => {
                    await fetch('/api/agent/stop', { method: 'POST' });
                  }}
                >
                  Stop
                </button>
              )}
            </div>
          </form>
        </div>
        
        {/* Agent Console */}
        <div className="bg-white rounded-lg shadow flex-grow overflow-hidden">
          <AgentConsole 
            logs={agentLogs} 
            status={agentStatus} 
            currentTask={currentTask} 
          />
        </div>
      </div>
      
      {/* Right Column - Browser Simulation and Results */}
      <div className="md:col-span-2 flex flex-col space-y-4">
        {/* Computer Simulation */}
        <div className="bg-gray-800 rounded-lg shadow-lg flex-grow overflow-hidden relative">
          <div className="absolute top-0 left-0 w-full p-3 flex justify-between items-center">
            <div className="flex space-x-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
            <div className="text-white text-xs">User's Computer</div>
          </div>
          
          <div className="h-full pt-8 pb-2 px-2">
            <div className="bg-white h-full rounded-md overflow-hidden border border-gray-300">
              <BrowserSimulation 
                activity={browserActivity} 
                isProcessing={isProcessing}
                queryResults={shoppingList}
              />
            </div>
          </div>
        </div>
        
        {/* Shopping Results */}
        {shoppingList.length > 0 && (
          <div className="bg-white rounded-lg shadow p-4">
            <ShoppingResults items={shoppingList} />
          </div>
        )}
      </div>
    </div>
  );
};

export default ShoppingAssistant;