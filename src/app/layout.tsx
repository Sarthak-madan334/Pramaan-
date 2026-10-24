import type { Metadata } from "next";
import "@fontsource-variable/manrope/index.css";
import "@fontsource/dm-mono/400.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "Pramaan — Proof behind every line",
  description: "An evidence-first career copilot for Indian students and freshers. Build a resume you can defend and choose where to apply with clarity.",
  openGraph: {
    title: "Pramaan — Proof behind every line",
    description: "Every claim deserves evidence. A more honest way to build your resume and plan your next move.",
    type: "website"
  }
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
