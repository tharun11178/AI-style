import React from "react";
import { RefreshCw } from "lucide-react";

export default function Loader({ label = "Loading advisor" }) {
  return (
    <main className="loading-screen">
      <RefreshCw className="spin" size={26} />
      <span>{label}</span>
    </main>
  );
}
