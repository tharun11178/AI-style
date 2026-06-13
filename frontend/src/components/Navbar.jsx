import React from "react";
import { LogOut, Sparkles, User } from "lucide-react";

export default function Navbar({ user, onLogout, title = "AI Style & Wellness Advisor" }) {
  return (
    <header className="topbar">
      <div>
        <p className="eyebrow">Dashboard</p>
        <h1>{title}</h1>
      </div>
      {user && (
        <div className="user-chip">
          <span>
            <User size={16} />
            {user.name}
          </span>
          <button onClick={onLogout} type="button" aria-label="Logout">
            <LogOut size={18} />
          </button>
        </div>
      )}
      {!user && (
        <span className="brand-mark small">
          <Sparkles size={18} />
        </span>
      )}
    </header>
  );
}
