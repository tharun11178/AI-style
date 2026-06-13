import React from "react";

export default function Dashboard({ stats = [], children }) {
  return (
    <div className="view-stack">
      <section className="stat-grid">
        {stats.map((stat) => (
          <article className="stat-card" key={stat.label}>
            <span>{stat.label}</span>
            <strong>{stat.value}</strong>
          </article>
        ))}
      </section>
      {children}
    </div>
  );
}
