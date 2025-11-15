"use client";

import { useState } from "react";

export default function UploadBox({ onSelect }) {
  const [preview, setPreview] = useState(null);

  function handleFile(e) {
    const file = e.target.files[0];
    if (!file) return;

    setPreview(URL.createObjectURL(file));
    onSelect(file);
  }

  return (
    <div className="text-center">
      {preview ? (
        <img
          src={preview}
          className="mx-auto rounded-lg max-h-52 object-cover mb-3"
        />
      ) : (
        <div className="p-10 text-gray-400">Upload an image</div>
      )}

      <input type="file" accept="image/*" onChange={handleFile} />
    </div>
  );
}
