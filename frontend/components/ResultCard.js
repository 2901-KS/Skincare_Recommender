export default function ResultCard({ data }) {
  return (
    <div className="p-6 bg-white rounded-xl shadow">
      <h3 className="text-xl font-semibold mb-3">{data.title}</h3>

      <ul className="space-y-3">
        {data.steps.map((s, i) => (
          <li key={i} className="flex gap-3">
            <div className="w-8 h-8 bg-pastelMint rounded-full flex items-center justify-center">
              {i + 1}
            </div>

            <div>
              <div className="font-medium">{s.step}</div>
              <div className="text-xs text-gray-500">{s.detail}</div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
