class WebSocketService {
  constructor() {
    this.socket = null;
    this.onMessageCallbacks = {};
    this.connected = false;
  }

  connect(url = 'ws://localhost:5000/ws') {
    if (this.socket && this.connected) {
      return Promise.resolve();
    }

    return new Promise((resolve, reject) => {
      this.socket = new WebSocket(url);

      this.socket.onopen = () => {
        console.log('WebSocket connected');
        this.connected = true;
        resolve();
      };

      this.socket.onclose = (event) => {
        console.log('WebSocket disconnected', event);
        this.connected = false;
        setTimeout(() => this.connect(url), 3000); // Attempt to reconnect
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      };

      this.socket.onmessage = (message) => {
        try {
          const data = JSON.parse(message.data);
          const { type } = data;
          
          if (this.onMessageCallbacks[type]) {
            this.onMessageCallbacks[type].forEach(callback => callback(data));
          }
          
          // Also trigger general message callbacks
          if (this.onMessageCallbacks['message']) {
            this.onMessageCallbacks['message'].forEach(callback => callback(data));
          }
        } catch (error) {
          console.error('Error processing WebSocket message:', error);
        }
      };
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
      this.connected = false;
    }
  }

  on(type, callback) {
    if (!this.onMessageCallbacks[type]) {
      this.onMessageCallbacks[type] = [];
    }
    this.onMessageCallbacks[type].push(callback);
    
    // Return a function to unsubscribe
    return () => {
      this.onMessageCallbacks[type] = this.onMessageCallbacks[type].filter(
        cb => cb !== callback
      );
    };
  }

  send(type, data = {}) {
    if (!this.connected) {
      console.error('Cannot send message: WebSocket not connected');
      return false;
    }
    
    const message = JSON.stringify({
      type,
      ...data,
      timestamp: new Date().toISOString()
    });
    
    this.socket.send(message);
    return true;
  }
}

// Create a singleton instance
const webSocketService = new WebSocketService();

export default webSocketService;