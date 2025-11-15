"use client";

import ResultCard from "../../../components/ResultCard";

export default function RegimenResult() {
  const data = JSON.parse(localStorage.getItem("regimen_data"));

  if (!data)
    return <p>No regimen found. Upload a picture again.</p>;

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Your Regimen</h2>

      <ResultCard
        data={{
          title: "Daily AM/PM Regimen",
          steps: data.regimen.map((step) => ({
            step: step.step,
            detail: step.detail,
          })),
        }}
      />
    </div>
  );
}
