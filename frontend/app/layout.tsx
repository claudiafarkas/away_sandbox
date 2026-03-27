import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Away Sandbox",
  description: "Web sandbox for geospatial and itinerary experiments",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
