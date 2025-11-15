import "./globals.css";

export const metadata = {
  title: "DoMy Skincare",
  description: "AI-powered skincare assistant",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen text-gray-800">
        <header className="py-6 shadow-sm bg-white">
          <div className="container mx-auto flex justify-between items-center px-4">
            <h1 className="text-2xl font-semibold">DoMy Skincare</h1>

            <nav className="space-x-4 text-sm">
              <a href="/">Home</a>
              <a href="/recommend">Recommend</a>
              <a href="/regimen">Regimen</a>
              <a href="/ingredients">Ingredients</a>
              <a href="/compare">Compare</a>
            </nav>
          </div>
        </header>

        <main className="container mx-auto px-4 mt-6">{children}</main>
      </body>
    </html>
  );
}
