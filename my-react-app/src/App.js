import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState([]);
  const [welcomeMessage, setWelcomeMessage] = useState('Loading...');
  const [loaded, setLoaded] = useState(false);
  const endOfMessagesRef = useRef(null); // Ref para o elemento "sentinela"

  useEffect(() => {
    document.title = 'Bakery Bot';
    fetchWelcomeMessage();
  }, []);

  useEffect(() => {
    // Rolar para o elemento "sentinela" sempre que as mensagens forem atualizadas
    if (endOfMessagesRef.current) {
      endOfMessagesRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const suggestions = [
    "Hello there!",
    "What's on the menu?",
    "I don't like bots"
  ];

  const fetchWelcomeMessage = () => {
    const checkBackend = () => {
      axios.get('http://localhost:5000/api/welcome_message')
        .then(response => {
          setWelcomeMessage(response.data.message);
          setMessages([{ text: response.data.message, sender: 'bot_response' }]);
          setLoaded(true);
        })
        .catch(error => {
          console.error("There was an error!", error);
          // Retry after 3 seconds
          setTimeout(checkBackend, 3000);
        });
    };

    checkBackend();
  };

  const handleMessageSend = () => {
    if (inputValue.trim() === '') return;

    const userMessage = { text: inputValue, sender: 'user' };
    setMessages(prevMessages => [...prevMessages, userMessage]);

    axios.post('http://localhost:5000/api/chatbot', { message: inputValue })
      .then(response => {
        const botAnalysisMessage = {
          text: `Spell check: ${response.data.corrected_message}\nSentiment: ${response.data.sentiment}`,
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
    setLoaded(false);
    fetchWelcomeMessage();
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleMessageSend();
    }
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
        <div ref={endOfMessagesRef} /> {/* Elemento "sentinela" */}
      </div>
      <div className="input-container">
        <input
          type="text"
          placeholder="Type your message here..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress} // Adiciona o manipulador de evento para pressionar a tecla
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
      <div className="watermark">
        <a href="https://github.com/helenafnandes" target="_blank">Made by Helena</a>
      </div>
    </div>
  );
}

export default App;
