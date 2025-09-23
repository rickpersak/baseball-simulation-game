import React, { useState } from 'react';

function NewGameScreen({ onBack, onWorldCreated }) {
  const [saveName, setSaveName] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleCreateWorld = async () => {
    setLoading(true);
    setMessage('Generating world, this may take a moment...');
    try {
      const response = await fetch('http://localhost:5000/api/new_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ save_name: saveName }),
      });
      const data = await response.json();
      if (response.ok) {
        // On success, call the new handler to switch to team selection
        onWorldCreated(saveName);
      } else {
        setMessage(`Error: ${data.message}`);
        setLoading(false);
      }
    } catch (error) {
      setMessage(`Network Error: Could not connect to the server.`);
      setLoading(false);
      console.error('Error creating new game:', error);
    }
  };

  return (
    <div className="screen-container">
      <h2>Start a New Game</h2>
      <p>Enter a name for your new save file (no spaces).</p>
      <input
        type="text"
        className="text-input"
        value={saveName}
        onChange={(e) => setSaveName(e.target.value)}
        placeholder="e.g., MyDynasty"
        disabled={loading}
      />
      <button className="main-button" onClick={handleCreateWorld} disabled={loading || !saveName}>
        {loading ? 'Generating...' : 'Create World'}
      </button>
      <button className="main-button" onClick={onBack} disabled={loading}>Back to Main Menu</button>
      {message && <p className="status-message">{message}</p>}
    </div>
  );
}

export default NewGameScreen;