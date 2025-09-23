import React from 'react';

function CreditsScreen({ onBack }) {
  return (
    <div className="screen-container">
      <h2>Credits</h2>
      <p>Game Design: [Your Name]</p>
      <p>Programming: [Your Name]</p>
      <button className="main-button" onClick={onBack}>Back to Main Menu</button>
    </div>
  );
}

export default CreditsScreen;