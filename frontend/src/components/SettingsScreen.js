import React from 'react';

function SettingsScreen({ onBack }) {
  return (
    <div className="screen-container">
      <h2>Settings</h2>
      <p>Settings will be implemented here.</p>
      <p>(e.g., difficulty, simulation detail, etc.)</p>
      <button className="main-button" onClick={onBack}>Back to Main Menu</button>
    </div>
  );
}

export default SettingsScreen;