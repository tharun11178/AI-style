import React from "react";
import { ImagePlus } from "lucide-react";

export default function ImageUploader({ preview, onChange }) {
  return (
    <label className="upload-zone">
      {preview ? (
        <img src={preview} alt="Selected face preview" />
      ) : (
        <span>
          <ImagePlus size={28} />
          Select photo
        </span>
      )}
      <input type="file" accept="image/*" onChange={onChange} />
    </label>
  );
}
