import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Document Summarizer",
  description: "Local document summarization and insights extraction",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gradient-to-br from-slate-50 to-slate-100">
        {children}
      </body>
    </html>
  );
}
