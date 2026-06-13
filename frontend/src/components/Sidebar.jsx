import React from "react";
import { BookOpen, HeartPulse, History, ShieldCheck, Sparkles, User } from "lucide-react";

export default function Sidebar({ view, setView, user }) {
  const items = [
    ["advisor", "Advisor", Sparkles],
    ["history", "History", History],
    ["profile", "Profile", User],
    ["feedback", "Feedback", HeartPulse],
    ["guide", "Guide", BookOpen],
  ];

  if (user?.role === "admin") {
    items.push(["admin", "Admin", ShieldCheck]);
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-title">
        <span className="brand-mark small">
          <Sparkles size={18} />
        </span>
        <span>Advisor</span>
      </div>
      <nav>
        {items.map(([key, label, Icon]) => (
          <button key={key} className={view === key ? "active" : ""} onClick={() => setView(key)} type="button">
            <Icon size={18} />
            {label}
          </button>
        ))}
      </nav>
    </aside>
  );
}
