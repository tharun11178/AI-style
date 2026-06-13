import React from "react";
import { Upload } from "lucide-react";
import ImageUploader from "../components/ImageUploader.jsx";

export default function UploadPhoto({ preview, onFileChange, children }) {
  return (
    <section className="analysis-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Face analysis</p>
          <h2>Upload photo</h2>
        </div>
        <Upload size={22} />
      </div>
      <ImageUploader preview={preview} onChange={onFileChange} />
      {children}
    </section>
  );
}
