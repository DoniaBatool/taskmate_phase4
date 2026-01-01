import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'TaskMate AI - Your Intelligent Task Companion',
  description: 'Manage your tasks effortlessly with AI-powered natural language chat. TaskMate AI helps you organize, track, and complete your todos through simple conversations.',
  keywords: ['task management', 'AI assistant', 'todo app', 'productivity', 'GPT-4', 'chatbot'],
  authors: [{ name: 'TaskMate AI Team' }],
  openGraph: {
    title: 'TaskMate AI - Your Intelligent Task Companion',
    description: 'Chat naturally, manage effortlessly with AI-powered assistance',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
