# Universal Shopping Assistant

A modern AI-powered shopping assistant application built with React, Flask, and CrewAI.

## Features

- **Multi-Agent System**: Utilizes CrewAI to coordinate multiple specialized agents for better shopping recommendations
- **Real-time Updates**: Get live feedback as the agents work on your shopping requests
- **Versatile Shopping**: Handles groceries, tech products, travel bookings, and financial investments
- **Beautiful UI**: Modern, responsive interface built with React and Tailwind CSS

## Project Structure

The project consists of two main parts:

- **Frontend**: React application with modern UI components
- **Backend**: Flask server with CrewAI agents

## Getting Started

### Prerequisites

- Node.js (v14+)
- Python (v3.8+)
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file based on the `.env.example` template:
   ```
   cp .env.example .env
   ```

6. Update the `.env` file with your OpenAI API key

7. Start the backend server:
   ```
   python app.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

## Usage

1. Open your browser and go to `http://localhost:3000`
2. Type a shopping query in the input field (e.g., "I need groceries for a vegan dinner party")
3. Watch the agents work in real-time to generate your shopping list
4. View and manage your shopping list with the provided tools

## CrewAI Agents

The system uses several specialized agents:

- **Inventory Agent**: Analyzes current inventory and identifies needed items
- **Dietary Agent**: Filters items based on dietary preferences
- **Budget Agent**: Optimizes shopping lists based on budget constraints
- **Price Comparison Agent**: Finds the best prices across different stores
- **Browser Agent**: Simulates browsing different stores
- **Tech Product Agent**: Researches and recommends tech products
- **Travel Agent**: Researches and plans travel itineraries
- **Finance Agent**: Provides financial investment advice

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Framework for orchestrating role-playing agents
- [React](https://reactjs.org/) - Frontend library
- [Flask](https://flask.palletsprojects.com/) - Backend framework
- [OpenAI](https://openai.com/) - AI models

## Troubleshooting

### Common Issues:

1. **OpenAI API Key**: Ensure your API key is correctly set in the `.env` file
2. **CORS Issues**: The backend includes CORS handling, but if you encounter issues, ensure the frontend proxy is correctly set
3. **Dependencies**: If you encounter module errors, try reinstalling dependencies with `pip install -r requirements.txt`
4. **Socket Connection**: If real-time updates aren't working, check that both frontend and backend servers are running