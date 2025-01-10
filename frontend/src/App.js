import React from 'react';
import Chat from './components/Chat';
import DashboardLayout from './components/DashboardLayout';
import './styles/Chat.css';

const App = () => {
    return (
      <div>
        <DashboardLayout>
          <Chat />
        </DashboardLayout>
      </div>
    );
  };

export default App;