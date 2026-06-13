import React, { useState } from "react";
import { RefreshCw, User } from "lucide-react";
import { apiRequest } from "../services/api.js";

export default function Profile({ user, onUserUpdate }) {
  const [form, setForm] = useState({
    name: user?.name || "",
    favorite_style: user?.favorite_style || "Smart casual",
    profession: user?.profession || "Student",
    occasion_preference: user?.occasion_preference || "Everyday",
    wellness_focus: user?.wellness_focus || "Energy",
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  async function submit(event) {
    event.preventDefault();
    setSaving(true);
    setMessage("");
    try {
      const updated = await apiRequest("/users/profile", {
        method: "PUT",
        body: JSON.stringify(form),
      });
      onUserUpdate?.(updated);
      setMessage("Profile saved.");
    } catch (err) {
      setMessage(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="view-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Profile</p>
          <h2>Preferences and account details</h2>
        </div>
        <User size={22} />
      </div>
      <form className="profile-form" onSubmit={submit}>
        <label>
          Name
          <input value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} />
        </label>
        <label>
          Profession
          <input value={form.profession} onChange={(event) => setForm({ ...form, profession: event.target.value })} />
        </label>
        {message && <p className={message.includes("saved") ? "success-text" : "error-text"}>{message}</p>}
        <button className="primary-action" disabled={saving} type="submit">
          {saving ? <RefreshCw className="spin" size={18} /> : <User size={18} />}
          Save profile
        </button>
      </form>
    </section>
  );
}
