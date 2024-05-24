import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState([]);
  const [welcomeMessage, setWelcomeMessage] = useState('Loading...');
  const [loaded, setLoaded] = useState(false); // New state variable

  useEffect(() => {
    fetchWelcomeMessage();
  }, []);

  const suggestions = [
    "Hello there!",
    "What's on the menu?",
    "I don't like bots"
  ];

  const fetchWelcomeMessage = () => {
    axios.get('http://localhost:5000/api/welcome_message')
      .then(response => {
        setWelcomeMessage(response.data.message);
        setMessages([{ text: response.data.message, sender: 'bot_response' }]);
        setLoaded(true); // Set loaded to true when message is fetched
      })
      .catch(error => {
        console.error("There was an error!", error);
        setWelcomeMessage('Failed to fetch welcome message');
      });
  };

  const handleMessageSend = () => {
    if (inputValue.trim() === '') return;

    const userMessage = { text: inputValue, sender: 'user' };
    setMessages(prevMessages => [...prevMessages, userMessage]);

    axios.post('http://localhost:5000/api/chatbot', { message: inputValue })
      .then(response => {
        const botAnalysisMessage = {
            text: `Corrected Message: ${response.data.corrected_message}\nSentiment: ${response.data.sentiment}`,
            sender: 'bot_analysis'
        };
        const botResponseMessage = { text: response.data.response, sender: 'bot_response' };

        setMessages(prevMessages => [
          ...prevMessages,
          botAnalysisMessage,
          botResponseMessage
        ]);
      })
      .catch(error => {
        console.error("There was an error!", error);
      });

    setInputValue('');
  };

  const handleSuggestion = (suggestionText) => {
    setInputValue(suggestionText);
  };

  const handleNewChat = () => {
    setMessages([]);
    setLoaded(false); // Reset loaded state to false
    fetchWelcomeMessage();
  };


  return (
    <div className="chat-container">
      <div className="message-list">
        {!loaded && <div className="message bot_response">Loading...</div>}
        {loaded && messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.sender}`}
          >
            {message.text.split('\n').map((line, i) => (
              <span key={i}>
                {line}
                <br />
              </span>
            ))}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          placeholder="Type your message here..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        />
        <button onClick={handleMessageSend}>Send</button>
        <button onClick={handleNewChat}>New Chat</button>
      </div>
      <div className="suggestions-container">
        <div className="suggestions-title">SUGGESTIONS</div>
        <div className="suggestions-buttons">
          {suggestions.map((suggestion, index) => (
            <button key={index} onClick={() => handleSuggestion(suggestion)}>{suggestion}</button>
          ))}
        </div>
      </div>
    <div class="watermark">
    <a href="https://github.com/helenafnandes" target="_blank">Made by Helena</a>
  </div>
    </div>
  );
}

export default App;
