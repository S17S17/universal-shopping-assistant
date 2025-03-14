import React, { useState, useEffect } from 'react';

const BrowserSimulation = ({ activity, isProcessing, queryResults }) => {
  const [currentUrl, setCurrentUrl] = useState('https://shopping-assistant.ai');
  const [browserHistory, setBrowserHistory] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeStore, setActiveStore] = useState('');
  const [displayedItems, setDisplayedItems] = useState([]);
  
  // Update browser simulation based on activity
  useEffect(() => {
    if (activity && activity.type === 'navigation') {
      setCurrentUrl(activity.url);
      setBrowserHistory(prevHistory => [
        ...prevHistory,
        {
          id: Date.now(),
          url: activity.url,
          title: getPageTitle(activity.url),
          timestamp: new Date()
        }
      ]);
      
      // Extract search term from URL if present
      const searchMatch = activity.url.match(/[?&]q=([^&]+)/);
      if (searchMatch) {
        setSearchTerm(decodeURIComponent(searchMatch[1].replace(/\+/g, ' ')));
      }
      
      // Extract store name from URL
      const storeMatch = activity.url.match(/https?:\/\/(?:www\.)?([^\.]+)\./);
      if (storeMatch) {
        setActiveStore(capitalizeFirstLetter(storeMatch[1]));
      }
    }
  }, [activity]);
  
  // Update displayed items based on query results and active store
  useEffect(() => {
    if (queryResults && queryResults.length > 0) {
      if (activeStore) {
        // Filter items for the active store
        const storeItems = queryResults.filter(item => 
          item.store && item.store.toLowerCase().includes(activeStore.toLowerCase())
        );
        setDisplayedItems(storeItems.length > 0 ? storeItems : queryResults.slice(0, 3));
      } else {
        setDisplayedItems(queryResults.slice(0, 3));
      }
    }
  }, [queryResults, activeStore]);
  
  // Helper function to get page title from URL
  const getPageTitle = (url) => {
    const domain = url.replace(/https?:\/\/(?:www\.)?([^\/]+).*/, '$1');
    const searchMatch = url.match(/[?&]q=([^&]+)/);
    if (searchMatch) {
      const term = decodeURIComponent(searchMatch[1].replace(/\+/g, ' '));
      return `${term} - ${capitalizeFirstLetter(domain.split('.')[0])}`;
    }
    return capitalizeFirstLetter(domain.split('.')[0]);
  };
  
  // Helper function to capitalize first letter
  const capitalizeFirstLetter = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };
  
  // Format time
  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };
  
  return (
    <div className="h-full flex flex-col">
      {/* Browser Controls */}
      <div className="bg-gray-100 p-2 flex items-center space-x-2">
        <button className="p-1 rounded hover:bg-gray-200">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <button className="p-1 rounded hover:bg-gray-200">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
        <button className="p-1 rounded hover:bg-gray-200">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
        <div className="flex-1 flex items-center bg-white border border-gray-300 rounded-md px-3 py-1">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-gray-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            type="text" 
            value={currentUrl} 
            className="flex-1 outline-none text-sm"
            readOnly
          />
        </div>
      </div>

      {/* Browser Content */}
      <div className="flex-1 bg-white overflow-y-auto">
        {isProcessing ? (
          <>
            {/* Store Header Simulation */}
            {activeStore && (
              <div className={`${getStoreColor(activeStore)} text-white p-4 flex justify-between items-center`}>
                <div className="font-bold text-xl">{activeStore}</div>
                <div className="flex items-center space-x-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  <div className="w-8 h-8 rounded-full bg-gray-200"></div>
                </div>
              </div>
            )}

            {/* Search Bar Simulation */}
            {searchTerm && (
              <div className={`${getStoreColor(activeStore, true)} p-4 flex justify-center`}>
                <div className="w-full max-w-2xl relative">
                  <input 
                    type="text" 
                    value={searchTerm}
                    className="w-full py-2 px-4 pr-10 rounded-full outline-none"
                    readOnly
                  />
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 absolute right-3 top-2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
              </div>
            )}

            {/* Search Results */}
            {searchTerm && displayedItems.length > 0 && (
              <div className="p-4">
                <h3 className="text-xl font-semibold mb-4">Results for "{searchTerm}"</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {displayedItems.map((item, index) => (
                    <div key={index} className="border border-gray-200 rounded-md p-4 hover:shadow-md transition-shadow">
                      <div className="h-40 bg-gray-100 mb-3 flex items-center justify-center">
                        {/* This would be an actual image in a real implementation */}
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
                        </svg>
                      </div>
                      <h4 className="font-medium">{item.name}</h4>
                      <div className="text-lg font-bold mt-1">${item.price?.toFixed(2)}</div>
                      <div className="text-sm text-gray-500">{item.quantity} {item.unit}</div>
                      <button className={`mt-3 w-full ${getStoreButtonColor(activeStore)} text-white py-1 px-3 rounded-full text-sm hover:opacity-90`}>
                        Add to cart
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-gray-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            <p className="text-lg mb-2">Browser Simulation</p>
            <p className="text-sm text-center max-w-md">
              Enter a query and let the assistant search for you. You'll see the browser activity here in real-time.
            </p>
          </div>
        )}
      </div>

      {/* Browser History */}
      {browserHistory.length > 0 && (
        <div className="bg-gray-100 border-t border-gray-200 p-2">
          <h4 className="text-xs font-medium text-gray-500 uppercase mb-2">Browser History</h4>
          <div className="space-y-1 max-h-24 overflow-y-auto">
            {browserHistory.map(item => (
              <div key={item.id} className="flex items-center text-sm p-1 hover:bg-gray-200 rounded">
                <div className="w-4 h-4 bg-blue-500 rounded mr-2"></div>
                <div className="flex-1">
                  <div className="font-medium truncate">{item.title}</div>
                  <div className="text-xs text-gray-500 truncate">{item.url}</div>
                </div>
                <div className="text-xs text-gray-500 whitespace-nowrap">
                  {formatTime(item.timestamp)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Helper function to get store-specific colors
const getStoreColor = (store, lighter = false) => {
  const storeColors = {
    walmart: lighter ? 'bg-blue-500' : 'bg-blue-600',
    amazon: lighter ? 'bg-yellow-500' : 'bg-yellow-600',
    target: lighter ? 'bg-red-500' : 'bg-red-600',
    bestbuy: lighter ? 'bg-blue-500' : 'bg-blue-600',
    kroger: lighter ? 'bg-blue-500' : 'bg-blue-600',
    wholefood: lighter ? 'bg-green-500' : 'bg-green-600',
    wholefoods: lighter ? 'bg-green-500' : 'bg-green-600',
    newegg: lighter ? 'bg-orange-500' : 'bg-orange-600',
    expedia: lighter ? 'bg-blue-500' : 'bg-blue-600',
    booking: lighter ? 'bg-blue-500' : 'bg-blue-600',
    vanguard: lighter ? 'bg-red-500' : 'bg-red-600',
    fidelity: lighter ? 'bg-green-500' : 'bg-green-600',
  };
  
  // Convert store name to lowercase for matching
  const storeLower = store.toLowerCase();
  
  // Find the matching store color or use a default
  for (const [key, color] of Object.entries(storeColors)) {
    if (storeLower.includes(key)) {
      return color;
    }
  }
  
  // Default color
  return lighter ? 'bg-gray-500' : 'bg-gray-600';
};

// Helper function to get store-specific button colors
const getStoreButtonColor = (store) => {
  const storeColors = {
    walmart: 'bg-blue-600',
    amazon: 'bg-yellow-600',
    target: 'bg-red-600',
    bestbuy: 'bg-blue-600',
    kroger: 'bg-blue-600',
    wholefood: 'bg-green-600',
    wholefoods: 'bg-green-600',
    newegg: 'bg-orange-600',
    expedia: 'bg-blue-600',
    booking: 'bg-blue-600',
    vanguard: 'bg-red-600',
    fidelity: 'bg-green-600',
  };
  
  // Convert store name to lowercase for matching
  const storeLower = store.toLowerCase();
  
  // Find the matching store color or use a default
  for (const [key, color] of Object.entries(storeColors)) {
    if (storeLower.includes(key)) {
      return color;
    }
  }
  
  // Default color
  return 'bg-blue-600';
};

export default BrowserSimulation;