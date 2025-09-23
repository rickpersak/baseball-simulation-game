// File: frontend/src/App.js
import React, { useState } from 'react';
import './App.css';

import AppHeader from './components/AppHeader';
import MainMenu from './components/MainMenu';
import NewGameScreen from './components/NewGameScreen';
import LoadGameScreen from './components/LoadGameScreen';
import SettingsScreen from './components/SettingsScreen';
import CreditsScreen from './components/CreditsScreen';
import FranchiseHub from './components/FranchiseHub';
import TeamSelectionScreen from './components/TeamSelectionScreen';

function App() {
  const [currentView, setCurrentView] = useState('main_menu');
  const [activeSave, setActiveSave] = useState(null);

  const handleWorldCreated = (saveName) => { setActiveSave(saveName); setCurrentView('team_selection'); };
  const handleTeamSelected = () => { setCurrentView('franchise_hub'); };
  const handleLoadGame = (saveName) => { setActiveSave(saveName); setCurrentView('franchise_hub'); };
  const handleExitFranchise = () => { setActiveSave(null); setCurrentView('main_menu'); };

  const renderView = () => {
    // Add the 'content-box' className to each screen's container div
    switch (currentView) {
      case 'team_selection':
        return <div className="content-box"><TeamSelectionScreen saveName={activeSave} onTeamSelected={handleTeamSelected} /></div>;
      case 'franchise_hub':
        return <div className="content-box"><FranchiseHub saveName={activeSave} onExit={handleExitFranchise} /></div>;
      case 'load_game':
        return <div className="content-box"><LoadGameScreen onBack={() => setCurrentView('main_menu')} onGameSelect={handleLoadGame} /></div>;
      case 'new_game':
        return <div className="content-box"><NewGameScreen onBack={() => setCurrentView('main_menu')} onWorldCreated={handleWorldCreated} /></div>;
      case 'settings':
        return <div className="content-box"><SettingsScreen onBack={() => setCurrentView('main_menu')} /></div>;
      case 'credits':
        return <div className="content-box"><CreditsScreen onBack={() => setCurrentView('main_menu')} /></div>;
      case 'quit':
        return <div className="content-box"><div className="screen-container"><h2>Goodbye!</h2><p>You can safely close this browser tab now.</p></div></div>;
      case 'main_menu':
      default:
        return <div className="content-box"><MainMenu showNewGame={() => setCurrentView('new_game')} showLoadGame={() => setCurrentView('load_game')} showSettings={() => setCurrentView('settings')} showCredits={() => setCurrentView('credits')} showQuit={() => setCurrentView('quit')} /></div>;
    }
  };

  return (
    <div className="App">
      <AppHeader />
      <main className="main-content">
        {renderView()}
      </main>
    </div>
  );
}

export default App;