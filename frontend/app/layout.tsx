import "./globals.css";

export const metadata = {
  title: "Aura AI",
  description: "Autonomous AI orchestration platform"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}