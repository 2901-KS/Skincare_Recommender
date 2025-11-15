import Card from "../components/Card";

export default function Home() {
  const tiles = [
    { title: "AI Recommendation", href: "/recommend" },
    { title: "Regimen Builder", href: "/regimen" },
    { title: "Ingredient Checker", href: "/ingredients" },
    { title: "Product Compare", href: "/compare" },
  ];

  return (
    <div>
      <h2 className="text-3xl font-bold mb-4">Beauty Dashboard</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {tiles.map((t) => (
          <a href={t.href} key={t.title}>
            <Card>
              <h3 className="text-xl font-semibold">{t.title}</h3>
            </Card>
          </a>
        ))}
      </div>
    </div>
  );
}
