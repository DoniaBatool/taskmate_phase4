'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { Header } from '@/components/Header';
import { getToken, getUserIdFromToken } from '@/lib/auth';
import { apiFetch, AuthError } from '@/lib/api';

export default function ChatPage() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    const token = getToken();
    const user = getUserIdFromToken();
    
    if (!token || !user) {
      router.replace('/login');
      return;
    }
    
    setIsAuthenticated(true);
    setUserId(user);
  }, [router]);

  // ChatKit configuration for custom backend
  const [error, setError] = useState<string | null>(null);
  const apiUrl = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/chatkit`;
  const domainKey = process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || '';
  
  const { control } = useChatKit({
    api: {
      // Custom backend URL
      url: apiUrl,
      // Domain key for production allowlist
      ...(domainKey && { domainKey }),
      // Custom fetch to inject JWT authentication
      fetch: async (input, init) => {
        const token = getToken();
        return fetch(input, {
          ...init,
          headers: {
            ...init?.headers,
            ...(token && { 'Authorization': `Bearer ${token}` }),
          },
          credentials: 'include',
        });
      },
    },
    // Error handling
    onError: (err) => {
      console.error('ChatKit error:', err);
      setError('Failed to load chat. Please refresh the page.');
    },
  });

  if (!isAuthenticated || !userId) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-theme-secondary">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Header />
      <div className="flex min-h-screen">
        <div className="flex-1 px-2 sm:px-4 py-4 sm:py-8 lg:pl-0">
          <div className="mx-auto flex max-w-4xl flex-col gap-3 sm:gap-4 h-[calc(100vh-8rem)] sm:h-[calc(100vh-12rem)]">
            {/* Header */}
            <div className="flex items-center justify-between flex-wrap gap-2 px-2 sm:px-0">
              <div>
                <h1 className="text-xl sm:text-2xl lg:text-3xl font-bold text-theme-primary">
                  AI Chat Assistant
                </h1>
                <p className="text-xs sm:text-sm text-theme-secondary">
                  Chat naturally to manage your tasks with AI
                </p>
              </div>
            </div>

            {/* ChatKit Component */}
            {error ? (
              <div className="flex-1 rounded-2xl shadow-inner overflow-hidden p-8 bg-red-500/10 border border-red-500/20" style={{ minHeight: '500px' }}>
                <div className="text-center">
                  <p className="text-red-400 mb-4">{error}</p>
                  <button 
                    onClick={() => window.location.reload()} 
                    className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                  >
                    Refresh Page
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex-1 rounded-2xl shadow-inner overflow-hidden" style={{ minHeight: '500px', height: '100%' }}>
                <ChatKit 
                  control={control} 
                  style={{ height: '100%', width: '100%' }}
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
