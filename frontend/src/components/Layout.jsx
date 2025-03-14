import React from 'react';

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <header className="bg-gray-900 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Universal Shopping Assistant</h1>
          <nav className="space-x-4">
            <a href="/" className="hover:text-blue-300">Home</a>
            <a href="https://github.com/S17S17/universal-shopping-assistant" target="_blank" rel="noopener noreferrer" className="hover:text-blue-300">GitHub</a>
          </nav>
        </div>
      </header>
      
      <main className="flex-grow container mx-auto p-4">
        {children}
      </main>
      
      <footer className="bg-gray-900 text-white p-4">
        <div className="container mx-auto text-center">
          <p>© {new Date().getFullYear()} Universal Shopping Assistant</p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;