"use client";

import ResultCard from "../../../components/ResultCard";

export default function RecommendResult() {
  const data = JSON.parse(localStorage.getItem("recommend_data"));

  if (!data)
    return <p>No results found. Go back and upload a photo again.</p>;

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Your AI Results</h2>

      <ResultCard
        data={{
          title: "Recommended Products",
          steps: data.recommendations.map((p) => ({
            step: p.product,
            detail: p.reason,
          })),
        }}
      />
    </div>
  );
}
