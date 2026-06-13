import React from "react";
import { Sparkles } from "lucide-react";

export default function Home({ onStart }) {
  return (
    <main className="auth-screen">
      <section className="auth-panel">
        <div className="brand-row">
          <span className="brand-mark">
            <Sparkles size={21} />
          </span>
          <div>
            <p className="eyebrow">AI Personal Style & Wellness Advisor</p>
            <h1>Style analysis workspace</h1>
          </div>
        </div>
        <button className="primary-action" onClick={onStart} type="button">
          <Sparkles size={18} />
          Start analysis
        </button>
      </section>
    </main>
  );
}
