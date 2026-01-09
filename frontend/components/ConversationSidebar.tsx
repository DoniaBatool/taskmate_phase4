'use client';

import { useState, useEffect } from 'react';
import { apiFetch } from '@/lib/api';
import { MessageSquare, Plus, Menu, X, Trash2 } from 'lucide-react';

interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

interface ConversationSidebarProps {
  currentConversationId: number | null;
  onSelectConversation: (conversationId: number) => void;
  onNewChat: () => void;
}

export function ConversationSidebar({
  currentConversationId,
  onSelectConversation,
  onNewChat,
}: ConversationSidebarProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    loadConversations();
  }, []);

  async function loadConversations() {
    setLoading(true);
    try {
      // Fetch all user conversations
      const data = await apiFetch<{ conversations: Conversation[] }>('/api/conversations');
      setConversations(data.conversations || []);
    } catch (error: any) {
      console.error('Failed to load conversations:', error);
      console.error('Error details:', error?.message || error?.detail || JSON.stringify(error));
      setConversations([]);
    } finally {
      setLoading(false);
    }
  }

  function formatDate(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }

  function getConversationTitle(conv: Conversation): string {
    if (conv.title && conv.title !== 'New Chat') {
      // Truncate title if too long
      return conv.title.length > 30 ? conv.title.slice(0, 30) + '...' : conv.title;
    }
    return 'New Chat';
  }

  return (
    <>
      {/* Mobile Menu Button - positioned below header */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed top-20 left-4 z-50 p-2 rounded-lg shadow-lg transition-colors"
        style={{
          backgroundColor: 'var(--bg-secondary)',
          borderColor: 'var(--border-primary)',
          color: 'var(--text-primary)',
          border: '1px solid'
        }}
        aria-label={isOpen ? 'Close sidebar' : 'Open sidebar'}
      >
        {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </button>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed lg:static inset-y-0 left-0 z-40 w-80 flex flex-col transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
        style={{
          backgroundColor: 'var(--bg-primary)',
          borderRight: '1px solid var(--border-primary)'
        }}
      >
        {/* Header */}
        <div
          className="p-4"
          style={{
            borderBottom: '1px solid var(--border-primary)',
            backgroundColor: 'var(--bg-primary)'
          }}
        >
          <button
            onClick={() => {
              onNewChat();
              setIsOpen(false);
              // Refresh conversations list
              loadConversations();
            }}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200 shadow-md hover:shadow-lg font-medium"
          >
            <Plus className="w-5 h-5" />
            <span>New Chat</span>
          </button>
        </div>

        {/* Conversations List */}
        <div
          className="flex-1 overflow-y-auto p-3 space-y-2"
          style={{ backgroundColor: 'var(--bg-secondary)' }}
        >
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div
                className="h-8 w-8 animate-spin rounded-full border-4 border-t-blue-600"
                style={{ borderColor: 'var(--border-primary)' }}
              />
            </div>
          ) : conversations.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center px-4">
              <MessageSquare
                className="w-12 h-12 mb-3"
                style={{ color: 'var(--text-tertiary)' }}
              />
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                No conversations yet
              </p>
              <p className="text-xs mt-1" style={{ color: 'var(--text-tertiary)' }}>
                Start a new chat to begin
              </p>
            </div>
          ) : (
            conversations.map((conversation) => {
              const isActive = conversation.id === currentConversationId;
              return (
                <button
                  key={conversation.id}
                  onClick={() => {
                    onSelectConversation(conversation.id);
                    setIsOpen(false);
                  }}
                  className={`w-full text-left px-3 py-3 rounded-lg transition-all duration-200 group ${
                    isActive
                      ? 'bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200'
                      : 'border hover:opacity-80'
                  }`}
                  style={
                    isActive
                      ? {}
                      : {
                          backgroundColor: 'var(--card-bg)',
                          borderColor: 'var(--card-border)',
                        }
                  }
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <MessageSquare
                          className="w-4 h-4 flex-shrink-0"
                          style={{
                            color: isActive
                              ? '#3b82f6'
                              : 'var(--text-tertiary)',
                          }}
                        />
                        <p
                          className="text-sm font-medium truncate"
                          style={{
                            color: isActive
                              ? '#1e40af'
                              : 'var(--text-primary)',
                          }}
                        >
                          {getConversationTitle(conversation)}
                        </p>
                      </div>
                      <p
                        className="text-xs truncate"
                        style={{
                          color: isActive
                            ? '#2563eb'
                            : 'var(--text-secondary)',
                        }}
                      >
                        {formatDate(conversation.updated_at)}
                        {conversation.message_count > 0 &&
                          ` · ${conversation.message_count} messages`}
                      </p>
                    </div>
                    {isActive && (
                      <div className="w-2 h-2 rounded-full bg-blue-600 flex-shrink-0 mt-1.5" />
                    )}
                  </div>
                </button>
              );
            })
          )}
        </div>

        {/* Footer */}
        <div
          className="p-3 text-center"
          style={{
            borderTop: '1px solid var(--border-primary)',
            backgroundColor: 'var(--bg-primary)',
          }}
        >
          <div className="text-xs" style={{ color: 'var(--text-tertiary)' }}>
            {conversations.length} conversation{conversations.length !== 1 ? 's' : ''}
          </div>
        </div>
      </div>
    </>
  );
}
