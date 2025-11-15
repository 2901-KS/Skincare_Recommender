export default function Card({ children }) {
  return (
    <div className="p-6 bg-white rounded-2xl shadow-md border">
      {children}
    </div>
  );
}
