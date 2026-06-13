import React, { useState } from "react";
import { RefreshCw, User } from "lucide-react";
import { login } from "../services/authService.js";

export default function Login({ onLogin }) {
  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      onLogin(await login(form));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="auth-form" onSubmit={submit}>
      <label>
        Email
        <input type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} />
      </label>
      <label>
        Password
        <input
          type="password"
          value={form.password}
          onChange={(event) => setForm({ ...form, password: event.target.value })}
        />
      </label>
      {error && <p className="error-text">{error}</p>}
      <button className="primary-action" disabled={loading} type="submit">
        {loading ? <RefreshCw className="spin" size={18} /> : <User size={18} />}
        Enter dashboard
      </button>
    </form>
  );
}
