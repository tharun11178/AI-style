import React from "react";
import OutfitCard from "../components/OutfitCard.jsx";

export default function OutfitRecommendations({ recommendations }) {
  return (
    <section className="view-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Outfits</p>
          <h2>Outfit recommendations</h2>
        </div>
      </div>
      <OutfitCard outfits={recommendations?.outfits || []} accessories={recommendations?.accessories || []} />
    </section>
  );
}
