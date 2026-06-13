import React from "react";
import { History as HistoryIcon } from "lucide-react";

export default function History({ history = [], onSelect, onDelete }) {
  return (
    <section className="view-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Recommendation history</p>
          <h2>Saved analyses</h2>
        </div>
        <HistoryIcon size={22} />
      </div>
      {history.length === 0 ? (
        <p className="muted">No analyses saved yet.</p>
      ) : (
        <div className="history-list">
          {history.map((item) => (
            <article key={item.id} className="history-card">
              <div>
                <h3>{item.face_shape} face shape</h3>
                <p>{item.skin_tone} tone</p>
              </div>
              <div className="history-actions">
                <button onClick={() => onSelect?.(item)} type="button">
                  Review
                </button>
                <button onClick={() => onDelete?.(item.id)} type="button" className="ghost-danger">
                  Delete
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
