export default function ProductCard({ product }) {
  return (
    <div className="p-4 rounded-xl bg-white shadow-md border">
      <h4 className="font-semibold">{product.name}</h4>
      <p className="text-sm text-gray-500 mt-2">{product.desc}</p>
    </div>
  );
}
