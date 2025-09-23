// File: frontend/src/components/TeamDetailPanel.js
import React, { useState, useEffect } from 'react';

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(value || 0);
};

const PlayerRating = ({ player }) => {
    const isPitcher = player.position === 'P';
    
    // Calculate overall ratings on 20-80 scale in increments of 5
    const snapTo5 = (rating) => Math.round(rating / 5) * 5;
    
    const currentOverall = isPitcher 
        ? snapTo5((player.stuff_current + player.movement_current + player.control_current) / 3)
        : snapTo5((player.contact_current + player.power_current + player.eye_current) / 3);
    
    const potentialOverall = isPitcher 
        ? snapTo5((player.stuff_potential + player.movement_potential + player.control_potential) / 3)
        : snapTo5((player.contact_potential + player.power_potential + player.eye_potential) / 3);
    
    // Function to get rating color class based on value
    const getRatingClass = (rating) => {
        if (rating >= 70) return 'rating-outstanding'; // Blue: 70-100+
        if (rating >= 60) return 'rating-excellent';   // Teal: 60-69
        if (rating >= 50) return 'rating-good';        // Green: 50-59
        if (rating >= 40) return 'rating-average';     // Yellow: 40-49
        if (rating >= 30) return 'rating-poor';        // Orange: 30-39
        return 'rating-awful';                         // Red: 20-29
    };
    
    // Function to get individual rating color class
    const getIndividualRatingClass = (current, potential) => {
        const avgRating = (current + potential) / 2;
        return getRatingClass(avgRating);
    };
    
    const rating1 = isPitcher ? `STU: ${player.stuff_current}/${player.stuff_potential}` : `CON: ${player.contact_current}/${player.contact_potential}`;
    const rating2 = isPitcher ? `MOV: ${player.movement_current}/${player.movement_potential}` : `POW: ${player.power_current}/${player.power_potential}`;
    const rating3 = isPitcher ? `CTL: ${player.control_current}/${player.control_potential}` : `EYE: ${player.eye_current}/${player.eye_potential}`;
    const clutchRating = `CLU: ${player.clutchness_current}/${player.clutchness_potential}`;
    
    // Get color classes for individual ratings
    const rating1Class = isPitcher 
        ? getIndividualRatingClass(player.stuff_current, player.stuff_potential)
        : getIndividualRatingClass(player.contact_current, player.contact_potential);
    const rating2Class = isPitcher 
        ? getIndividualRatingClass(player.movement_current, player.movement_potential)
        : getIndividualRatingClass(player.power_current, player.power_potential);
    const rating3Class = isPitcher 
        ? getIndividualRatingClass(player.control_current, player.control_potential)
        : getIndividualRatingClass(player.eye_current, player.eye_potential);
    const clutchClass = getIndividualRatingClass(player.clutchness_current, player.clutchness_potential);
    
    return (
        <div className="player-card">
            <div className="player-header">
                <div className="player-info">
                    <span className="player-name">{player.first_name} {player.last_name}</span>
                    <span className="player-details">({player.age}, {player.position})</span>
                </div>
                <div className="player-overall">
                    <div className={`rating-pair ${getRatingClass(currentOverall)}`}>
                        <span className="rating-label">Overall</span>
                        <span className="rating-value">{currentOverall}</span>
                    </div>
                    <div className={`rating-pair ${getRatingClass(potentialOverall)}`}>
                        <span className="rating-label">Potential</span>
                        <span className="rating-value">{potentialOverall}</span>
                    </div>
                </div>
            </div>
            <div className="player-ratings-grid">
                <div className={`rating-stat ${rating1Class}`}>{rating1}</div>
                <div className={`rating-stat ${rating2Class}`}>{rating2}</div>
                <div className={`rating-stat ${rating3Class}`}>{rating3}</div>
                <div className={`rating-stat ${clutchClass}`}>{clutchRating}</div>
            </div>
        </div>
    );
};

function TeamDetailPanel({ team, saveName, onConfirm }) {
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!team) return;
    const fetchDetails = async () => {
      setLoading(true);
      try {
        const response = await fetch(`http://localhost:5000/api/franchise/${saveName}/teams/${team.team_id}`);
        const data = await response.json();
        setDetails(data);
      } catch (error) {
        console.error("Error fetching team details:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchDetails();
  }, [saveName, team]);

  const handleConfirm = () => {
    onConfirm(team.team_id);
  };

  if (!team) {
    return (
      <div className="team-detail-panel">
        <h3>Select a Team</h3>
        <p>Click on a team from the list to see their details.</p>
      </div>
    );
  }

  return (
    <div className="team-detail-panel">
      <h3>{team.city} {team.nickname}</h3>
      <div className="panel-content-wrapper">
        {loading && <p>Loading details...</p>}
        {details && !details.error && (
          <div className="team-details-grid">
            {/* === THIS IS THE CORRECTED LINE === */}
            <div className="detail-item"><strong>Team Overall</strong><span>{team.team_overall} / 100</span></div>
            <div className="detail-item"><strong>Owner Goal</strong><span>{team.goal}</span></div>
            <div className="detail-item"><strong>Team Budget</strong><span>{formatCurrency(team.budget)}</span></div>
            <div className="detail-item"><strong>Current Payroll</strong><span>{formatCurrency(details.payroll)}</span></div>
            <div className="detail-item full-width">
              <strong>Top Players</strong>
              <div className="players-container">
                {details.top_players.map((p, index) => (
                  <PlayerRating key={index} player={p} />
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
      <div className="panel-actions">
        <button className="main-button" onClick={handleConfirm} disabled={loading}>Manage This Team</button>
      </div>
    </div>
  );
}

export default TeamDetailPanel;