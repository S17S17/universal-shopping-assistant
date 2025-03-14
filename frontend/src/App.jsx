import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Layout from './components/Layout';
import ShoppingAssistant from './components/ShoppingAssistant';
import './styles/global.css';

function App() {
  return (
    <Router>
      <Layout>
        <ShoppingAssistant />
      </Layout>
    </Router>
  );
}

export default App;