import React, { useState, useRef, useEffect } from 'react';
import { ChevronLeft, Send } from 'lucide-react';
import BankBuddyPig from './BankBuddyPig';

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

const Message = ({ text, isOutgoing }) => (
  <div className={`flex w-full ${isOutgoing ? 'justify-end' : 'justify-start'}`}>
    <div className={`max-w-[80%] px-4 py-2 rounded-[18px] whitespace-pre-wrap text-[15px] leading-relaxed
      ${isOutgoing 
        ? 'bg-blue-800 text-white ml-auto' 
        : 'bg-slate-100 text-slate-800 mr-auto'}`}
    >
      {text}
    </div>
  </div>
);

const MessageInput = ({ onSend }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSend(message.trim());
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
        className="flex-1 px-4 py-2 border-2 border-blue-700 rounded-full focus:outline-none focus:border-blue-700 text-[15px]"
      />
      <button 
        type="submit" 
        className="p-2 hover:opacity-80 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
        disabled={!message.trim()}
      >
        <Send size={20} color={message.trim() ? '#003DA5' : '#94A3B8'} />
      </button>
    </form>
  );
};

const Chat = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hi there! How can I help you today?", isOutgoing: false }
  ]);
  
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (text) => {
    // Add user message immediately
    const newUserMessage = { id: messages.length + 1, text, isOutgoing: true };
    setMessages(prev => [...prev, newUserMessage]);

    try {
      // Call the chatbot API
      const response = await fetch('http://localhost:8000/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, stream: false })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const botResponse = {
        id: messages.length + 2,
        text: data.reply,
        isOutgoing: false
      };

      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      console.error("Error calling chatbot API:", error);
      const errorResponse = {
        id: messages.length + 2,
        text: "Sorry, there was an error processing your request.",
        isOutgoing: false
      };
      setMessages(prev => [...prev, errorResponse]);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white border border-blue-900 rounded-3xl shadow-md">
      <Header />
      <div className="flex-1 overflow-y-auto p-4 space-y-2 bg-white">
        {messages.map((message) => (
          <Message key={message.id} text={message.text} isOutgoing={message.isOutgoing} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      <MessageInput onSend={handleSendMessage} />
    </div>
  );
};

export default Chat;
