import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "LawCo AI - Your Intelligent Legal Assistant",
  description:
    "Get instant legal insights, document analysis, and professional guidance through our advanced AI-powered chatbot. Upload documents, ask questions, and receive comprehensive legal assistance.",
  keywords: [
    "AI",
    "legal assistant",
    "document analysis",
    "chatbot",
    "legal advice",
    "law",
    "legal technology",
  ],
  authors: [{ name: "LawCo AI Team" }],
  creator: "LawCo AI",
  publisher: "LawCo AI",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL("https://lawco-ai.com"),
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "LawCo AI - Your Intelligent Legal Assistant",
    description:
      "Get instant legal insights, document analysis, and professional guidance through our advanced AI-powered chatbot.",
    url: "https://lawco-ai.com",
    siteName: "LawCo AI",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "LawCo AI - Intelligent Legal Assistant",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "LawCo AI - Your Intelligent Legal Assistant",
    description:
      "Get instant legal insights, document analysis, and professional guidance through our advanced AI-powered chatbot.",
    images: ["/og-image.jpg"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <meta name="theme-color" content="#3B82F6" />
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1, maximum-scale=1"
        />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-white`}
      >
        {children}
      </body>
    </html>
  );
}
