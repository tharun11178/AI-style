import React from "react";
import { Scissors } from "lucide-react";

export default function HairstyleCard({ hairstyles = [], beard }) {
  const items = beard ? [...hairstyles, beard] : hairstyles;
  return (
    <article className="recommendation-card">
      <div className="recommendation-title">
        <Scissors size={18} />
        <h3>Hair and beard</h3>
      </div>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </article>
  );
}
