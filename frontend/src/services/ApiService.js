const API_BASE_URL = 'http://localhost:5000/api';

class ApiService {
  async handleResponse(response) {
    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      const error = new Error(
        errorData?.message || `API error: ${response.status} ${response.statusText}`
      );
      error.status = response.status;
      error.data = errorData;
      throw error;
    }
    
    return response.json();
  }

  async sendQuery(query, context = {}) {
    const response = await fetch(`${API_BASE_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        context,
      }),
    });
    
    return this.handleResponse(response);
  }
  
  async getShoppingList() {
    const response = await fetch(`${API_BASE_URL}/shopping-list`);
    return this.handleResponse(response);
  }
  
  async getAgentStatus() {
    const response = await fetch(`${API_BASE_URL}/agent-status`);
    return this.handleResponse(response);
  }
  
  async getRecentQueries() {
    const response = await fetch(`${API_BASE_URL}/recent-queries`);
    return this.handleResponse(response);
  }
  
  async getTechProducts() {
    const response = await fetch(`${API_BASE_URL}/tech-products`);
    return this.handleResponse(response);
  }
  
  async getTravelOptions() {
    const response = await fetch(`${API_BASE_URL}/travel-options`);
    return this.handleResponse(response);
  }
  
  async getFinancialAdvice() {
    const response = await fetch(`${API_BASE_URL}/financial-advice`);
    return this.handleResponse(response);
  }
  
  async getBrowserHistory() {
    const response = await fetch(`${API_BASE_URL}/browser-history`);
    return this.handleResponse(response);
  }
  
  async saveShoppingList(items) {
    const response = await fetch(`${API_BASE_URL}/shopping-list`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ items }),
    });
    
    return this.handleResponse(response);
  }
  
  async checkout(items) {
    const response = await fetch(`${API_BASE_URL}/checkout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ items }),
    });
    
    return this.handleResponse(response);
  }
}

// Create a singleton instance
const apiService = new ApiService();

export default apiService;