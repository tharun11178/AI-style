import React from "react";
import { Palette } from "lucide-react";

export default function ColorPalette({ palette }) {
  if (!palette) {
    return null;
  }

  return (
    <article className="palette-card">
      <div className="recommendation-title">
        <Palette size={18} />
        <h3>{palette.name}</h3>
      </div>
      <div className="swatches">
        {palette.colors.map((color) => (
          <span key={color} style={{ backgroundColor: color }} title={color} />
        ))}
      </div>
    </article>
  );
}
