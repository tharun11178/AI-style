import React from "react";
import { Shirt } from "lucide-react";

export default function OutfitCard({ outfits = [], accessories = [] }) {
  return (
    <article className="recommendation-card">
      <div className="recommendation-title">
        <Shirt size={18} />
        <h3>Outfit recommendations</h3>
      </div>
      <ul>
        {[...outfits, ...accessories].map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </article>
  );
}
