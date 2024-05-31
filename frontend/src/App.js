import React, { useEffect, useState } from 'react';
import Keycloak from 'keycloak-js';
import axios from 'axios';
import './App.css';

function App() {
  const [keycloak, setKeycloak] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    const keycloak = new Keycloak({
      url: 'http://localhost:8080/',
      realm: 'master2',
      clientId: 'react'
    });

    keycloak.init({ onLoad: 'login-required' }).then(authenticated => {
      setKeycloak(keycloak);
      setAuthenticated(authenticated);
      if (authenticated) {
        keycloak.loadUserInfo().then(userInfo => {
          console.log('User Info:', userInfo);
        });
        fetchMessages(keycloak.token);
      }
    });
  }, []);

  const fetchMessages = async (token) => {
    const response = await axios.get('http://localhost:5000/messages', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    setMessages(response.data);
  };

  const handleMessageSubmit = async (e) => {
    e.preventDefault();
    if (newMessage.trim()) {
      await axios.post('http://localhost:5000/messages', { content: newMessage }, {
        headers: {
          'Authorization': `Bearer ${keycloak.token}`
        }
      });
      setNewMessage('');
      fetchMessages(keycloak.token);
    }
  };

  if (!keycloak) {
    return <div>Initializing Keycloak...</div>;
  }

  if (!authenticated) {
    return <div>Unable to authenticate!</div>;
  }

  return (
    <div className="App">
      <h1>Message Board</h1>
      <form onSubmit={handleMessageSubmit}>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
      <ul>
        {messages.map((msg, index) => (
          <li key={index}>
            <strong>{msg.user}</strong>: {msg.content}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
