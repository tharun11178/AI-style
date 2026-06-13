import React from "react";
import { Gauge } from "lucide-react";

export default function FaceAnalysis({ analysis }) {
  if (!analysis) {
    return null;
  }

  return (
    <section className="result-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Face result</p>
          <h2>{analysis.face_shape} face shape</h2>
        </div>
        <Gauge size={22} />
      </div>
      <div className="score-grid">
        <div>
          <span>Symmetry</span>
          <strong>{Math.round(analysis.symmetry_score)}%</strong>
        </div>
        <div>
          <span>Jawline</span>
          <strong>{Math.round(analysis.jawline_score)}%</strong>
        </div>
        <div>
          <span>Contrast</span>
          <strong>{analysis.contrast_level}</strong>
        </div>
        <div>
          <span>Skin tone</span>
          <strong>{analysis.skin_tone}</strong>
        </div>
      </div>
    </section>
  );
}
