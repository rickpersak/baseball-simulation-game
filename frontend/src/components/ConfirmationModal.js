// File: frontend/src/components/ConfirmationModal.js
import React from 'react';

function ConfirmationModal({ message, onConfirm, onCancel }) {
  // We stop the click from propagating to the backdrop to prevent accidental closing.
  const handleModalContentClick = (e) => {
    e.stopPropagation();
  };

  return (
    // The backdrop covers the whole screen and closes the modal when clicked.
    <div className="modal-backdrop" onClick={onCancel}>
      <div className="modal-content confirmation-modal" onClick={handleModalContentClick}>
        <h3>Confirm Action</h3>
        <p className="confirmation-message">{message}</p>
        <div className="modal-actions">
          <button className="main-button delete-button" onClick={onConfirm}>
            Confirm Delete
          </button>
          <button className="main-button secondary" onClick={onCancel}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmationModal;