import React from "react";
import HairstyleCard from "../components/HairstyleCard.jsx";

export default function HairstyleRecommendations({ recommendations }) {
  return (
    <section className="view-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Hairstyles</p>
          <h2>Hairstyle recommendations</h2>
        </div>
      </div>
      <HairstyleCard hairstyles={recommendations?.hairstyles || []} beard={recommendations?.beard} />
    </section>
  );
}
