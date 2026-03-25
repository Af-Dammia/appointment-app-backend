// frontend/src/components/Dashboard.js
import React, { useEffect, useState } from "react";
import API from "../services/api";
import AppointmentForm from "./AppointmentForm";
import AppointmentList from "./AppointmentList";
import "../styles/Dashboard.css";

const Dashboard = () => {
  const [appointments, setAppointments] = useState([]);
  const [editing, setEditing] = useState(null);

const handleUpdate = () => {
  fetchAppointments();  // refresh list
  setEditing(null);     // reset editing state
};

  const fetchAppointments = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await API.get("/appointments", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setAppointments(res.data);
    } catch (err) {
      console.log(err.response?.data);
      alert("Failed to fetch appointments");
    }
  };

  useEffect(() => {
    fetchAppointments();
  }, []);

  const handleAdd = (appointment) => {
    setAppointments((prev) => [...prev, appointment]);
  };

  const handleDelete = (id) => {
    setAppointments((prev) => prev.filter((a) => a.id !== id));
  };

  const handleCancelEdit = () => {
  setEditing(null); // this resets the editing state
 };

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Appointments Dashboard</h1>
      <div className="dashboard-content">
        <div className="form-section">
          <AppointmentForm
            onAdd={handleAdd}
            editing={editing}
            onUpdate={handleUpdate}
            onCancel={handleCancelEdit} 
         />
        </div>
        <div className="list-section">
          <h2>Existing Appointments</h2>
          <AppointmentList 
             appointments={appointments}
             onDelete={handleDelete}
             onEdit={setEditing}
              />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;