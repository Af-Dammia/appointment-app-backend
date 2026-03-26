import React, { useState } from "react";
import API from "../services/api";
import ConfirmModal from "./ConfirmModal";
import "../styles/Dashboard.css";

const AppointmentList = ({ appointments, onDelete, onEdit }) => {
  const [showModal, setShowModal] = useState(false);
  const [selectedId, setSelectedId] = useState(null);

  const handleDeleteClick = (id) => {
    setSelectedId(id);
    setShowModal(true); // open modal
  };

  const handleConfirmDelete = async () => {
    try {
      const token = localStorage.getItem("token");
      await API.delete(`/appointments/${selectedId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      onDelete(selectedId);
    } catch (err) {
      console.log(err.response?.data);
      alert("Failed to delete appointment");
    } finally {
      setShowModal(false);
      setSelectedId(null);
    }
  };

  const handleCancelDelete = () => {
    setShowModal(false);
    setSelectedId(null);
  };

  return (
    <div className="appointment-container">
      <h2 className="appointment-heading">Appointments</h2>

      {appointments.length === 0 ? (
        <p className="empty-text">No appointments yet.</p>
      ) : (
        <ul className="appointment-list">
          {appointments.map((a) => (
            <li key={a.id} className="appointment-card">
              <div className="appointment-info">
                <p className="appointment-title">{a.title}</p>
                <p className="appointment-desc">{a.description}</p>
                <p className="appointment-date">{new Date(a.appointment_date).toLocaleString("de-DE", {
                        year: "numeric",
                        month: "short",
                        day: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                        })}</p>
              </div>
              <div className="card-actions">
              <button onClick={() => onEdit(a)} className="edit-btn"> ✏️</button>
              <button onClick={() => handleDeleteClick(a.id)} className="delete-btn"> × </button>
              </div>
            </li>
          ))}
        </ul>
      )}

      {showModal && (
        <ConfirmModal
          message="Are you sure you want to delete this appointment?"
          onConfirm={handleConfirmDelete}
          onCancel={handleCancelDelete}
        />
      )}
    </div>
  );
};

export default AppointmentList;