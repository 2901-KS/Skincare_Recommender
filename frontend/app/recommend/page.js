"use client";

import { useState } from "react";
import UploadBox from "../../components/UploadBox";
import { sendPrediction } from "../../services/recommend";

export default function RecommendPage() {
  const [file, setFile] = useState(null);

  async function handleSubmit() {
    if (!file) return alert("Upload a selfie first!");

    const res = await sendPrediction(file, false, 0);
    localStorage.setItem("recommend_data", JSON.stringify(res));

    window.location.href = "/recommend/result";
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">AI Recommendation</h2>

      <UploadBox onSelect={setFile} />

      <button
        onClick={handleSubmit}
        className="mt-6 px-4 py-2 bg-primary text-white rounded-md"
      >
        Get Recommendation
      </button>
    </div>
  );
}
