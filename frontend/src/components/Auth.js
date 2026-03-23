import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // <-- import this
import API from "../services/api";
import "../styles/Auth.css";

function Auth() {
  const navigate = useNavigate(); // <-- add this
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setError("");
    setUsername("");
    setEmail("");
    setPassword("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      if (isLogin) {
        const formData = new URLSearchParams();
        formData.append("username", username);
        formData.append("password", password);
        formData.append("grant_type", "password");

        const res = await API.post("/auth/login", formData, {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });

        localStorage.setItem("token", res.data.access_token);
        navigate("/dashboard"); // <-- redirect to dashboard
      } else {
        const res = await API.post("/auth/register", {
          username,
          email,
          password,
        });

        localStorage.setItem("token", res.data.access_token);
        navigate("/dashboard"); // <-- redirect to dashboard
      }
    } catch (err) {
      setError(isLogin ? "Login failed" : "Registration failed");
      console.error(err);
    }
  };

  return (
    <div className="auth-container">
      <h2>{isLogin ? "Login" : "Register"}</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        {!isLogin && (
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        )}
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">{isLogin ? "Login" : "Register"}</button>
      </form>
      <p>
        {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
        <span className="toggle-link" onClick={toggleMode}>
          {isLogin ? "Register" : "Login"}
        </span>
      </p>
    </div>
  );
}

export default Auth;