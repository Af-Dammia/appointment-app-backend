import React, { useState, useEffect } from "react";
import API from "../services/api";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css"; // import styles

const AppointmentForm = ({ onAdd, editing, onUpdate, onCancel }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [date, setDate] = useState(null); // use JS Date object

  // Fill form when editing
  useEffect(() => {
    if (editing) {
      setTitle(editing.title);
      setDescription(editing.description || "");
      setDate(new Date(editing.appointment_date));
    } else {
      setTitle("");
      setDescription("");
      setDate(null);
    }
  }, [editing]);

  const handleCancel = () => {
    setTitle("");
    setDescription("");
    setDate(null);      // clear the date
    if (onCancel) onCancel(); // tell parent we canceled
 };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      const payload = {
        title,
        description,
        appointment_date: date,
      };

      if (editing) {
        await API.put(`/appointments/${editing.id}`, payload, {
          headers: { Authorization: `Bearer ${token}` },
        });
        onUpdate();
      } else {
        const res = await API.post("/appointments", payload, {
          headers: { Authorization: `Bearer ${token}` },
        });
        onAdd(res.data);
      }

      setTitle("");
      setDescription("");
      setDate(null);

    } catch (err) {
      console.log(err.response?.data);
      alert("Operation failed");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h2 className="form-heading">
        {editing ? "Edit Appointment" : "Add Appointment"}
      </h2>

      <input
        type="text"
        placeholder="Enter title..."
        className="form-input"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />

      {/* Modern Date Picker */}
      <DatePicker
        selected={date}
        onChange={(d) => setDate(d)}
        showTimeSelect
        timeFormat="HH:mm"
        timeIntervals={15}
        dateFormat="MMMM d, yyyy h:mm aa"
        placeholderText="Select date and time"
        className="form-input"
        required
      />

      <textarea
        placeholder="Enter description..."
        className="form-textarea"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <button className="form-button" type="submit">
        {editing ? "Update Appointment" : "+ Add Appointment"}
      </button>

      {editing && (
        <button type="button" className="cancel-btn" onClick={handleCancel}>
          Cancel
        </button>
      )}
    </form>
  );
};

export default AppointmentForm;