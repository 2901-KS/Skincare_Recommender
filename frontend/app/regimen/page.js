"use client";

import { useState } from "react";
import UploadBox from "../../components/UploadBox";
import { sendRegimen } from "../../services/recommend";

export default function RegimenPage() {
  const [file, setFile] = useState(null);

  async function handleSubmit() {
    if (!file) return alert("Upload a selfie first!");

    const res = await sendRegimen(file, false, 0);
    localStorage.setItem("regimen_data", JSON.stringify(res));

    window.location.href = "/regimen/result";
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Build Your Regimen</h2>

      <UploadBox onSelect={setFile} />

      <button
        onClick={handleSubmit}
        className="mt-6 px-4 py-2 bg-primary text-white rounded-md"
      >
        Generate Regimen
      </button>
    </div>
  );
}
