import React, { useState } from 'react';

const ShoppingResults = ({ items }) => {
  const [groupBy, setGroupBy] = useState('store');
  
  // Group items by the selected criterion
  const groupedItems = items.reduce((groups, item) => {
    const key = item[groupBy] || 'Other';
    if (!groups[key]) {
      groups[key] = [];
    }
    groups[key].push(item);
    return groups;
  }, {});
  
  // Calculate total cost
  const totalCost = items.reduce((sum, item) => sum + (item.price * (item.quantity || 1)), 0);
  
  // Determine if we have special items (tech, travel, finance)
  const itemCategories = items.map(item => item.category?.toLowerCase() || '');
  const hasTechItems = itemCategories.some(cat => 
    ['laptop', 'smartphone', 'computer', 'tablet', 'electronics'].includes(cat)
  );
  const hasTravelItems = itemCategories.some(cat => 
    ['hotel', 'flight', 'resort', 'airbnb'].includes(cat)
  );
  const hasFinanceItems = itemCategories.some(cat => 
    ['etf', 'stock', 'fund', 'bond', 'crypto'].includes(cat)
  );
  
  // Get the result type
  const resultType = hasTechItems ? 'Tech Products' : 
                     hasTravelItems ? 'Travel Options' : 
                     hasFinanceItems ? 'Investment Options' : 'Shopping List';
  
  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">{resultType} Results</h3>
        <div className="flex items-center space-x-2">
          <label htmlFor="groupBy" className="text-sm text-gray-600">Group by:</label>
          <select
            id="groupBy"
            value={groupBy}
            onChange={(e) => setGroupBy(e.target.value)}
            className="text-sm border border-gray-300 rounded px-2 py-1"
          >
            <option value="store">Store</option>
            <option value="category">Category</option>
          </select>
        </div>
      </div>
      
      <div className="space-y-4">
        {Object.entries(groupedItems).map(([group, groupItems]) => (
          <div key={group} className="border border-gray-200 rounded-lg overflow-hidden">
            <div className="bg-gray-100 px-4 py-2 font-medium flex justify-between items-center">
              <span>{group}</span>
              <span className="text-sm text-gray-600">{groupItems.length} items</span>
            </div>
            <div className="divide-y divide-gray-200">
              {groupItems.map((item, index) => (
                <div key={index} className="px-4 py-3 flex justify-between items-center">
                  <div className="flex-1">
                    <div className="font-medium">{item.name}</div>
                    <div className="text-sm text-gray-600">
                      {item.quantity} {item.unit} {groupBy === 'store' && item.category && `• ${item.category}`}
                      {groupBy === 'category' && item.store && `• ${item.store}`}
                      {item.specs && `• ${item.specs}`}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-bold">${item.price?.toFixed(2)}</div>
                    <div className="text-sm text-gray-600">
                      ${(item.price * (item.quantity || 1)).toFixed(2)} total
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 border-t border-gray-200 pt-4 flex justify-between items-center">
        <div>
          <span className="text-gray-600">Total Items:</span> {items.length}
        </div>
        <div className="text-right">
          <span className="text-gray-600">Total Cost:</span> <span className="font-bold">${totalCost.toFixed(2)}</span>
        </div>
      </div>
      
      <div className="mt-4 flex space-x-2 justify-end">
        <button className="px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50">
          Save Results
        </button>
        <button className="px-4 py-2 bg-blue-600 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-blue-700">
          {hasTechItems ? 'Purchase Selected' : 
           hasTravelItems ? 'Book Selected' : 
           hasFinanceItems ? 'Invest Now' : 'Checkout'}
        </button>
      </div>
    </div>
  );
};

export default ShoppingResults;