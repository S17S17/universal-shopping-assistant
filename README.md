# Universal Shopping Assistant

A comprehensive shopping assistant that handles grocery and non-grocery shopping with a Manus-like UI.

## Features

- **Universal Shopping Assistant**: Handles both grocery and non-grocery queries
- **Price Comparison**: Compare prices across multiple stores
- **Product Recommendations**: Get personalized product recommendations
- **Smart Shopping List**: Automatically generate shopping lists based on inventory
- **Budget Optimization**: Optimize your shopping to stay within budget
- **Dietary Preferences**: Filter products based on dietary preferences
- **Travel Planning**: Get travel recommendations and compare prices
- **Tech Product Research**: Compare specifications and prices for electronics
- **Financial Advisory**: Get investment recommendations and financial advice

## UI Features

- **Manus-like Interface**: A modern UI with a computer simulation showing the agent at work
- **Real-Time Browser Simulation**: Watch the agent search and navigate websites
- **Agent Console**: View real-time logs and activities
- **Shopping Dashboard**: Track your shopping history and preferences

## Technology Stack

- **Backend**: Python, Flask, CrewAI, LangChain
- **Frontend**: React, TailwindCSS
- **Browser Automation**: browser-use library
- **AI Models**: OpenAI GPT-4o

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- OpenAI API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/S17S17/universal-shopping-assistant.git
cd universal-shopping-assistant
```

2. Set up the backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Edit this file to add your API keys
```

3. Set up the frontend
```bash
cd ../frontend
npm install
cp .env.example .env  # Edit this file if needed
```

### Running the Application

1. Start the backend server
```bash
cd backend
python app.py
```

2. Start the frontend server
```bash
cd ../frontend
npm start
```

3. Open your browser and navigate to http://localhost:3000

## License

[MIT](LICENSE)