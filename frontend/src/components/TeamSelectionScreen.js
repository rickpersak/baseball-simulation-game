// File: frontend/src/components/TeamSelectionScreen.js
import React, { useState, useEffect } from 'react';
import TeamDetailPanel from './TeamDetailPanel'; // Import the new panel

function TeamSelectionScreen({ saveName, onTeamSelected }) {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTeam, setSelectedTeam] = useState(null); // This team will be shown in the detail panel

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/franchise/${saveName}/teams`);
        const data = await response.json();
        setTeams(data);
      } catch (error) {
        console.error("Error fetching teams:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchTeams();
  }, [saveName]);

  const handleSelectTeam = async (teamId) => {
    try {
      await fetch(`http://localhost:5000/api/franchise/${saveName}/select_team`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ team_id: teamId }),
      });
      onTeamSelected();
    } catch (error) {
      console.error("Failed to select team:", error);
    }
  };

  if (loading) return <div className="screen-container"><h2>Loading Teams...</h2></div>;

  return (
    <div className="screen-container">
      <h2>Choose Your Team</h2>
      <p>Select a team from the list to view their details and begin your career.</p>
      <div className="team-selection-container">
        {/* Master Panel (Left) */}
        <div className="team-list-panel scrollable">
          <table>
            <thead>
              <tr>
                <th>Team Name</th>
                <th>Overall</th>
                <th>Budget</th>
                <th>Goal</th>
              </tr>
            </thead>
            <tbody>
              {teams.map(team => (
                <tr key={team.team_id} onClick={() => setSelectedTeam(team)} className={selectedTeam?.team_id === team.team_id ? 'selected' : ''}>
                  <td>{team.city} {team.nickname}</td>
                  <td>{team.team_overall}</td>
                  <td>${(team.budget / 1_000_000).toFixed(0)}M</td>
                  <td>{team.goal}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {/* Detail Panel (Right) */}
        <TeamDetailPanel 
          team={selectedTeam} 
          saveName={saveName} 
          onConfirm={handleSelectTeam} 
        />
      </div>
    </div>
  );
}

export default TeamSelectionScreen;