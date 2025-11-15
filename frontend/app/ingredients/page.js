"use client";

import { useState } from "react";
import { checkIngredients } from "../../services/analysis";

export default function Ingredients() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  async function analyze() {
    const res = await checkIngredients({
      ingredients: text,
      acne_level: 2,
      skin_type: 1,
      skin_tone: 1,
      sensitive: false,
    });

    setResult(res.analysis);
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-3">Ingredient Checker</h2>

      <textarea
        className="w-full p-3 border rounded-md"
        rows={4}
        placeholder="Enter ingredients list..."
        onChange={(e) => setText(e.target.value)}
      ></textarea>

      <button
        onClick={analyze}
        className="mt-4 px-4 py-2 bg-primary text-white rounded-md"
      >
        Analyze
      </button>

      {result && (
        <div className="mt-6 p-4 bg-white shadow rounded-xl">
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
