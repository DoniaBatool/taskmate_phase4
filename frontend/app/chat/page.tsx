'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Header } from '@/components/Header';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';
import { apiFetch, AuthError } from '@/lib/api';
import { getToken, getUserIdFromToken } from '@/lib/auth';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!getToken()) {
      router.replace('/login');
      return;
    }

    // Fetch latest conversation from database (true stateless architecture)
    loadLatestConversation();
  }, [router]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  async function loadLatestConversation() {
    setLoadingHistory(true);
    try {
      // Fetch user's most recent conversation from database
      const conversation = await apiFetch<{
        conversation_id: number | null;
        messages: Array<{ role: string; content: string; created_at: string }>;
      }>('/api/conversations/latest');

      if (conversation.conversation_id) {
        setConversationId(conversation.conversation_id);

        if (conversation.messages && conversation.messages.length > 0) {
          const loadedMessages: Message[] = conversation.messages.map(msg => ({
            role: msg.role as 'user' | 'assistant',
            content: msg.content,
            timestamp: new Date(msg.created_at),
          }));
          setMessages(loadedMessages);
        }
      }
    } catch (err: any) {
      if (err instanceof AuthError) {
        router.replace('/login');
        return;
      }
      console.error('Failed to load latest conversation:', err);
      // Start fresh if unable to load
      setConversationId(null);
      setMessages([]);
    } finally {
      setLoadingHistory(false);
    }
  }

  async function sendMessage(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || loading) return;

    // Get user ID from JWT token
    const userId = getUserIdFromToken();
    if (!userId) {
      router.replace('/login');
      return;
    }

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await apiFetch<{
        response: string;
        conversation_id: number;
      }>(`/api/${userId}/chat`, {
        method: 'POST',
        body: JSON.stringify({
          message: userMessage.content,
          conversation_id: conversationId,
        }),
      });

      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id);
        // No localStorage - conversation persists in database only
      }

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err: any) {
      if (err instanceof AuthError) {
        router.replace('/login');
        return;
      }

      const errorMessage: Message = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${err?.message || 'Unknown error'}. Please try again.`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  }

  function startNewConversation() {
    setMessages([]);
    setConversationId(null);
    setInput('');
    // No localStorage to clear - state only in database
  }

  return (
    <>
      <Header />
      <div className="min-h-screen px-4 py-8">
        <div className="mx-auto flex max-w-4xl flex-col gap-4 h-[calc(100vh-12rem)]">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-theme-primary">AI Chat Assistant</h1>
              <p className="text-sm text-theme-secondary">
                Chat naturally to manage your tasks with AI
              </p>
            </div>
            {messages.length > 0 && (
              <Button onClick={startNewConversation} variant="secondary">
                New Chat
              </Button>
            )}
          </div>

          {/* Chat Messages - iMessage Style */}
          <div className="flex-1 overflow-hidden rounded-2xl chat-background shadow-inner">
            <div className="h-full overflow-y-auto p-4 space-y-3">
              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <div className="relative mb-6">
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full blur-xl opacity-30 animate-pulse"></div>
                    <div className="relative bg-gradient-to-br from-blue-500 to-purple-600 p-5 rounded-full">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={2}
                        stroke="currentColor"
                        className="w-10 h-10 text-white"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                    </div>
                  </div>
                  <h2 className="text-2xl font-bold text-theme-primary mb-3">
                    TaskMate AI
                  </h2>
                  <p className="text-theme-secondary max-w-md mb-6">
                    Your intelligent task assistant is ready to help
                  </p>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-lg">
                    {[
                      { icon: '➕', text: 'Add task to buy groceries', color: 'from-blue-500 to-blue-600' },
                      { icon: '📋', text: 'Show my tasks', color: 'from-purple-500 to-purple-600' },
                      { icon: '✓', text: 'Mark task as complete', color: 'from-green-500 to-green-600' },
                      { icon: '✏️', text: 'Update task details', color: 'from-orange-500 to-orange-600' },
                    ].map((suggestion, i) => (
                      <button
                        key={i}
                        onClick={() => setInput(suggestion.text)}
                        className={`bg-gradient-to-r ${suggestion.color} text-white px-4 py-2 rounded-xl text-sm font-medium hover:shadow-lg transform hover:scale-105 transition-all duration-200`}
                      >
                        <span className="mr-2">{suggestion.icon}</span>
                        {suggestion.text}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <>
                  {messages.map((message, index) => (
                    <div
                      key={index}
                      className={`flex gap-2 items-end animate-fadeIn ${
                        message.role === 'user' ? 'justify-end' : 'justify-start'
                      }`}
                    >
                      {/* Assistant Avatar */}
                      {message.role === 'assistant' && (
                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            strokeWidth={2}
                            stroke="currentColor"
                            className="w-5 h-5 text-white"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z"
                            />
                          </svg>
                        </div>
                      )}

                      {/* Message Bubble */}
                      <div className="flex flex-col max-w-[75%]">
                        <div
                          className={`rounded-2xl px-4 py-2.5 shadow-sm ${
                            message.role === 'user'
                              ? 'bg-gradient-to-br from-blue-500 to-purple-600 text-white rounded-br-sm'
                              : 'message-bubble-assistant rounded-bl-sm'
                          }`}
                        >
                          <p className="text-[15px] leading-relaxed whitespace-pre-wrap">
                            {message.content}
                          </p>
                        </div>
                        {message.timestamp && (
                          <p
                            className={`text-xs mt-1 px-1 ${
                              message.role === 'user' ? 'text-right' : 'text-left'
                            } text-slate-500 dark:text-slate-400`}
                          >
                            {message.timestamp.toLocaleTimeString([], {
                              hour: '2-digit',
                              minute: '2-digit',
                            })}
                          </p>
                        )}
                      </div>

                      {/* Spacer for user messages (no avatar) */}
                      {message.role === 'user' && <div className="w-8" />}
                    </div>
                  ))}

                  {/* Typing Indicator */}
                  {loading && (
                    <div className="flex gap-2 items-end animate-fadeIn">
                      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                          strokeWidth={2}
                          stroke="currentColor"
                          className="w-5 h-5 text-white"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z"
                          />
                        </svg>
                      </div>
                      <div className="message-bubble-assistant rounded-2xl rounded-bl-sm px-5 py-3 shadow-sm">
                        <div className="flex items-center gap-1">
                          <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                          <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </>
              )}
            </div>
          </div>

          {/* Input Form - iOS Style */}
          <form onSubmit={sendMessage} className="flex gap-3 items-end">
            <div className="flex-1 relative">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="iMessage"
                className="chat-input w-full rounded-3xl px-5 py-3 pr-12 text-[15px] focus:outline-none transition-colors shadow-sm"
                disabled={loading}
              />
              {input.trim() && !loading && (
                <button
                  type="button"
                  onClick={() => setInput('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth={2}
                    stroke="currentColor"
                    className="w-5 h-5"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              )}
            </div>
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className={`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center transition-all duration-200 shadow-lg ${
                input.trim() && !loading
                  ? 'bg-gradient-to-br from-blue-500 to-purple-600 hover:shadow-xl hover:scale-105'
                  : 'bg-slate-300 dark:bg-slate-600 cursor-not-allowed'
              }`}
            >
              {loading ? (
                <svg
                  className="animate-spin h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
              ) : (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  className="w-5 h-5 text-white"
                >
                  <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
                </svg>
              )}
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
