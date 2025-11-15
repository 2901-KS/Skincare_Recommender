"use client";

import { useState } from "react";
import { compareProducts } from "../../services/analysis";

export default function ComparePage() {
  const [p1, setP1] = useState("");
  const [p2, setP2] = useState("");
  const [result, setResult] = useState(null);

  async function handleCompare() {
    const res = await compareProducts({
      product1: p1,
      product2: p2,
      acne_level: 2,
      skin_type: 1,
      skin_tone: 1,
      sensitive: false,
    });

    setResult(res.comparison);
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Compare Products</h2>

      <input
        className="border p-2 w-full mb-2"
        placeholder="Product 1"
        onChange={(e) => setP1(e.target.value)}
      />
      <input
        className="border p-2 w-full mb-2"
        placeholder="Product 2"
        onChange={(e) => setP2(e.target.value)}
      />

      <button
        onClick={handleCompare}
        className="px-4 py-2 bg-primary text-white rounded-md"
      >
        Compare
      </button>

      {result && (
        <div className="mt-4 p-4 bg-white shadow rounded-xl">
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
