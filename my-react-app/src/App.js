// src/App.js
import React, { useEffect, useState } from 'react';

/*
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/api/data')
      .then(response => {
        setData(response.data.message);
      })
      .catch(error => {
        console.error("There was an error!", error);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p>{data}</p>
      </header>
    </div>
  );
}

export default App;
*/
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I assist you today?", sender: "bot" }
  ]);
  const [inputValue, setInputValue] = useState("");

  const handleMessageSend = () => {
    if (inputValue.trim() !== "") {
      const newMessage = { text: inputValue, sender: "user" };
      setMessages([...messages, newMessage]);
      setInputValue("");
      // Simulate bot response (replace with actual bot response logic)
      setTimeout(() => {
        const botResponse = [
          { text: "I'm sorry, I didn't understand. Can you please rephrase?", sender: "bot" },
          { text: "Alternatively, you can ask me about something else.", sender: "bot" }
        ];
        setMessages([...messages, ...botResponse]);
      }, 1000);
    }
  };

  return (
    <div className="chat-container">
      <div className="message-list">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.sender}`}
          >
            {message.text}
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
      </div>
    </div>
  );
}

export default App;
