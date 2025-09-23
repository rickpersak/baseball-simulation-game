import React from 'react';
import '../App.css';

function MainMenu({ showNewGame, showLoadGame, showSettings, showCredits, showQuit }) {
  return (
    <div className="menu-container">
      <h1>Baseball Sim Game</h1>
      <button className="main-button" onClick={showNewGame}>Start New Game</button>
      <button className="main-button" onClick={showLoadGame}>Load Game</button>
      <button className="main-button" onClick={showSettings}>Settings</button>
      <button className="main-button" onClick={showCredits}>Credits</button>
      <button className="main-button" onClick={showQuit}>Quit Game</button>
    </div>
  );
}

export default MainMenu;