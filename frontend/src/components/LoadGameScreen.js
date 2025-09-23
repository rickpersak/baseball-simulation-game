// File: frontend/src/components/LoadGameScreen.js
import React, { useState, useEffect } from 'react';
import ConfirmationModal from './ConfirmationModal'; // Import the new component

function LoadGameScreen({ onBack, onGameSelect }) {
  const [saveFiles, setSaveFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  // --- NEW STATE FOR MODAL CONTROL ---
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [targetToDelete, setTargetToDelete] = useState(null);

  const fetchSaves = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/api/saves");
      const data = await response.json();
      setSaveFiles(data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setMessage("Failed to fetch save files.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSaves();
  }, []);

  // --- NEW HANDLERS FOR MODAL ---
  const handleDeleteClick = (fileName) => {
    // Instead of confirming immediately, we set the target and show the modal
    setTargetToDelete(fileName);
    setIsModalVisible(true);
  };

  const handleConfirmDelete = async () => {
    if (!targetToDelete) return;
    
    const saveName = targetToDelete.replace('.db', '');
    setMessage(`Deleting ${saveName}...`);
    setIsModalVisible(false); // Hide the modal

    try {
      const response = await fetch(`http://localhost:5000/api/saves/${saveName}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(`'${saveName}' was successfully deleted.`);
        fetchSaves(); // Refresh the list
      } else {
        setMessage(`Error: ${data.message}`);
      }
    } catch (error) {
      setMessage("Failed to connect to the server for deletion.");
      console.error("Error deleting file:", error);
    } finally {
      setTargetToDelete(null); // Clear the target
    }
  };

  const handleCancelDelete = () => {
    setIsModalVisible(false);
    setTargetToDelete(null);
  };
  
  return (
    <> {/* Use a Fragment to render modal alongside the screen */}
      <div className="screen-container">
        <h2>Load Game</h2>
        <div className="list-container">
          {loading && <p>Loading saves...</p>}
          {!loading && saveFiles.length > 0 ? (
            <ul>
              {saveFiles.map((file, index) => (
                <li key={index} className="load-game-item">
                  <span className="save-name-text">{file.replace('.db', '')}</span>
                  <div className="button-group">
                    <button className="main-button load-button" onClick={() => onGameSelect(file.replace('.db', ''))}>
                      Load
                    </button>
                    {/* This button now just opens the modal */}
                    <button className="main-button delete-button" onClick={() => handleDeleteClick(file)}>
                      Delete
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            !loading && <p>No save files found.</p>
          )}
        </div>
        {message && <p className="status-message">{message}</p>}
        <button className="main-button" onClick={onBack}>Back to Main Menu</button>
      </div>

      {/* --- RENDER THE MODAL CONDITIONALLY --- */}
      {isModalVisible && (
        <ConfirmationModal
          message={`Are you sure you want to permanently delete '${targetToDelete.replace('.db', '')}'? This action cannot be undone.`}
          onConfirm={handleConfirmDelete}
          onCancel={handleCancelDelete}
        />
      )}
    </>
  );
}

export default LoadGameScreen;