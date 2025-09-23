// File: frontend/src/components/FranchiseHub.js
import React, { useState, useEffect } from 'react';

function FranchiseHub({ saveName, onExit }) {
  const [franchiseData, setFranchiseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [simMessage, setSimMessage] = useState('');

  const fetchData = async () => {
    setLoading(true);
    setSimMessage('');
    try {
      const response = await fetch(`http://localhost:5000/api/franchise/${saveName}`);
      if (!response.ok) throw new Error("Failed to fetch franchise data");
      const data = await response.json();
      setFranchiseData(data);
    } catch (error) {
      console.error("Error fetching franchise data:", error);
      setFranchiseData({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [saveName]);

  const handleSimulate = async () => {
    setSimMessage('Simulating game, please wait...');
    try {
      const response = await fetch(`http://localhost:5000/api/franchise/${saveName}/simulate`, { method: 'POST' });
      const data = await response.json();
      const result = data.result;
      const message = result ? `Sim complete. Final Score: Away ${result.away_score} - Home ${result.home_score}` : data.message;
      setSimMessage(message || `Simulation finished.`);
      fetchData(); // Refresh all data after simulation
    } catch (error) {
      setSimMessage('Simulation failed.');
      console.error("Error simulating game:", error);
    }
  };

  if (loading) {
    return <div className="screen-container"><h2>Loading Franchise: {saveName}...</h2></div>;
  }

  if (!franchiseData || franchiseData.error) {
    return (
      <div className="screen-container">
        <h2>Error Loading Franchise</h2>
        <p>{franchiseData?.error || "An unknown error occurred."}</p>
        <button className="main-button" onClick={onExit}>Back to Main Menu</button>
      </div>
    );
  }

  const { team, standings, next_game } = franchiseData;

  return (
    <div className="screen-container hub-container">
      <div className="hub-header">
        <h2>{team.city} {team.nickname}</h2>
        <button className="main-button" onClick={onExit}>Exit to Main Menu</button>
      </div>
      
      <div className="hub-main-area">
        <div className="hub-controls">
          <h3>Season Control</h3>
          {next_game ? (
            <div className="next-game-box">
              <p><strong>Next Game: Day {next_game.day}</strong></p>
              <p>{next_game.away_city} {next_game.away_nickname}</p>
              <p>at</p>
              <p>{next_game.home_city} {next_game.home_nickname}</p>
            </div>
          ) : (
            <div className="next-game-box"><p><strong>Season is complete!</strong></p></div>
          )}
          <button className="main-button" onClick={handleSimulate} disabled={!next_game}>Simulate Next Game</button>
          {simMessage && <p className="status-message">{simMessage}</p>}
        </div>

        <div className="hub-standings">
          <h3>League Standings</h3>
          <div className="list-container scrollable">
            <table>
              <thead>
                <tr><th>Team</th><th>W</th><th>L</th></tr>
              </thead>
              <tbody>
                {standings.map((t, i) => (
                  <tr key={i}>
                    <td>{t.city} {t.nickname}</td>
                    <td>{t.wins}</td>
                    <td>{t.losses}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default FranchiseHub;