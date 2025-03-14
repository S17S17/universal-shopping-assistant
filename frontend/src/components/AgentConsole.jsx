import React, { useRef, useEffect } from 'react';

const AgentConsole = ({ logs, status, currentTask }) => {
  const consoleRef = useRef(null);
  
  // Auto-scroll to the bottom when logs are updated
  useEffect(() => {
    if (consoleRef.current) {
      consoleRef.current.scrollTop = consoleRef.current.scrollHeight;
    }
  }, [logs]);
  
  // Format timestamp
  const formatTime = (timestamp) => {
    const date = new Date(timestamp * 1000);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };
  
  // Get appropriate icon for log type
  const getLogIcon = (type) => {
    switch (type) {
      case 'success':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      case 'warning':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        );
      case 'error':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      case 'info':
      default:
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
    }
  };
  
  return (
    <div className="h-full flex flex-col">
      <div className="bg-gray-800 text-white p-3">
        <h2 className="text-lg font-semibold flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
          </svg>
          Agent Console
        </h2>
        <div className="text-sm text-gray-400">Current Task: {currentTask}</div>
      </div>
      
      {/* Agent Status Section */}
      <div className="bg-gray-700 p-3">
        <h3 className="text-sm font-medium text-gray-300 mb-2">Agent Status</h3>
        <div className="grid grid-cols-2 gap-2">
          {Object.entries(status).map(([agent, state]) => (
            <div key={agent} className="flex items-center">
              <div className={`w-2 h-2 rounded-full mr-2 ${getStatusColor(state)}`}></div>
              <span className="text-xs text-gray-300 capitalize">{formatAgentName(agent)}: {state}</span>
            </div>
          ))}
        </div>
      </div>
      
      {/* Console Log Section */}
      <div 
        ref={consoleRef}
        className="flex-1 bg-black text-green-400 p-3 font-mono text-xs overflow-y-auto"
      >
        {logs.map((log, index) => (
          <div key={index} className="mb-1 flex items-start">
            <span className="text-gray-500 mr-2 whitespace-nowrap">[{formatTime(log.timestamp)}]</span>
            <span className="mr-2 mt-0.5">{getLogIcon(log.type)}</span>
            <span>{log.message}</span>
          </div>
        ))}
        
        {/* Blinking cursor */}
        <div className="flex items-center">
          <span className="text-gray-500 mr-2 whitespace-nowrap">[{formatTime(Date.now() / 1000)}]</span>
          <span className="mr-2 text-green-500">></span>
          <span className="animate-pulse">_</span>
        </div>
      </div>
    </div>
  );
};

// Helper function to get status color
const getStatusColor = (state) => {
  switch (state) {
    case 'active':
      return 'bg-green-500';
    case 'initializing':
      return 'bg-yellow-500';
    case 'error':
      return 'bg-red-500';
    case 'idle':
    default:
      return 'bg-gray-500';
  }
};

// Helper function to format agent name
const formatAgentName = (name) => {
  // Convert snake_case to Title Case
  return name
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

export default AgentConsole;