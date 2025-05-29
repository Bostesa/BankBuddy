import React, { useState, useRef, useEffect } from 'react';
import { ChevronLeft, Send, Loader } from 'lucide-react';
import BankBuddyPig from './BankBuddyPig';
import { chatAPI } from '../services/api';

const Header = () => (
  <div className="flex items-center p-3 border-b border-slate-200 bg-white rounded-3xl">
    <button className="p-2 hover:bg-slate-100 rounded-full transition-colors">
      <ChevronLeft size={20} className="text-slate-700"/>
    </button>
    <div className="ml-2">
      <BankBuddyPig />
    </div>
  </div>
);

const Message = ({ text, isOutgoing, isLoading }) => (
  <div className={`flex w-full ${isOutgoing ? 'justify-end' : 'justify-start'}`}>
    <div className={`max-w-[80%] px-4 py-2 rounded-[18px] whitespace-pre-wrap text-[15px] leading-relaxed
      ${isOutgoing 
        ? 'bg-blue-800 text-white ml-auto' 
        : 'bg-slate-100 text-slate-800 mr-auto'}`}
    >
      {isLoading ? (
        <div className="flex items-center space-x-2">
          <Loader className="animate-spin" size={16} />
          <span>Thinking...</span>
        </div>
      ) : (
        text
      )}
    </div>
  </div>
);

const ErrorMessage = ({ message, onRetry }) => (
  <div className="flex items-center justify-center p-2 my-2 bg-red-50 text-red-600 rounded-lg">
    <span className="text-sm">{message}</span>
    {onRetry && (
      <button 
        onClick={onRetry}
        className="ml-2 text-sm underline hover:text-red-700"
      >
        Retry
      </button>
    )}
  </div>
);

const MessageInput = ({ onSend, disabled }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSend(message);
      setMessage('');
    }
  };

  return (
    <form 
      className="flex items-center gap-3 p-4 bg-white border-t border-slate-100 rounded-3xl"
      onSubmit={handleSubmit}
    >
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message..."
        disabled={disabled}
        className="flex-1 px-4 py-2 border-2 border-blue-700 rounded-full focus:outline-none focus:border-blue-700 text-[15px] disabled:opacity-50"
      />
      <button 
        type="submit" 
        className="p-2 hover:opacity-80 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
        disabled={!message.trim() || disabled}
      >
        <Send size={20} color={message.trim() && !disabled ? '#003DA5' : '#94A3B8'} />
      </button>
    </form>
  );
};

const Chat = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hi there! How can I help you today?", isOutgoing: false }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (text) => {
    console.log('Sending message:', text);
    
    const newUserMessage = {
      id: messages.length + 1,
      text,
      isOutgoing: true
    };
    
    setMessages(prev => [...prev, newUserMessage]);
    setIsLoading(true);
    setError(null);

    try {
      console.log('Making API request to backend...');
      const response = await chatAPI.sendMessage(text);
      console.log('Received response:', response);
      
      const botResponse = {
        id: messages.length + 2,
        text: response,
        isOutgoing: false
      };

      setMessages(prev => [...prev, botResponse]);
    } catch (err) {
      console.error('Error from API:', err);
      setError(err.message || 'Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  const handleRetry = () => {
    if (messages.length >= 2) {
      const lastUserMessage = messages[messages.length - (isLoading ? 2 : 1)];
      if (lastUserMessage.isOutgoing) {
        handleSendMessage(lastUserMessage.text);
      }
    }
  };

  return (
    <div className="flex flex-col h-full bg-white border border-blue-900 rounded-3xl shadow-md">
      <Header />
      <div className="flex-1 overflow-y-auto p-4 space-y-2 bg-white">
        {messages.map((message) => (
          <Message
            key={message.id}
            text={message.text}
            isOutgoing={message.isOutgoing}
          />
        ))}
        {isLoading && (
          <Message
            text=""
            isOutgoing={false}
            isLoading={true}
          />
        )}
        {error && (
          <ErrorMessage 
            message={error}
            onRetry={handleRetry}
          />
        )}
        <div ref={messagesEndRef} />
      </div>
      <MessageInput 
        onSend={handleSendMessage}
        disabled={isLoading}
      />
    </div>
  );
};

export default Chat;
