import React, { useState } from "react";
import { RefreshCw, User } from "lucide-react";
import { registerAccount } from "../services/authService.js";

export default function Register({ onRegister }) {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      onRegister(await registerAccount(form));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="auth-form" onSubmit={submit}>
      <label>
        Name
        <input value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} />
      </label>
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
        Create account
      </button>
    </form>
  );
}
