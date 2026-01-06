# Frontend - Todo Chatbot Phase 3

> **Next.js 14 + TypeScript + Tailwind CSS + OpenAI ChatKit**
> Modern, responsive web application with AI-powered natural language task management

---

## 📋 Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Frontend Agents](#frontend-agents)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Components](#components)
- [Pages & Routes](#pages--routes)
- [API Integration](#api-integration)
- [Authentication](#authentication)
- [Styling & Design](#styling--design)
- [Testing](#testing)
- [Deployment](#deployment)
- [Resources](#resources)

---

## 🎯 Overview

The **Frontend** is a Next.js 14 application built with TypeScript, Tailwind CSS, and shadcn/ui components. It provides a modern, responsive user interface for task management with AI-powered natural language interaction.

**Key Features:**
- ✅ User authentication (JWT-based)
- ✅ Task CRUD operations with traditional UI
- ✅ AI Chatbot for natural language task management
- ✅ Real-time conversation history
- ✅ Responsive design (mobile-first)
- ✅ Dark mode support
- ✅ Accessibility (WCAG AA compliant)
- ✅ Performance optimized (Core Web Vitals)

**Phase III Addition:**
- 🤖 **AI Chatbot Interface** - Natural language task management via OpenAI ChatKit
- 💬 **Conversation History** - Persistent chat sessions stored in PostgreSQL
- 🔄 **Seamless Integration** - Traditional UI + AI Chat in one cohesive experience

---

## 🛠️ Technology Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Framework** | Next.js 14 (App Router) | React framework with SSR/SSG |
| **Language** | TypeScript | Type safety and better DX |
| **Styling** | Tailwind CSS | Utility-first CSS framework |
| **UI Components** | shadcn/ui | Accessible component library |
| **Data Fetching** | React Query | Server state management |
| **AI Chat** | OpenAI ChatKit | Pre-built chat UI components |
| **Authentication** | JWT + localStorage | Token-based auth |
| **Deployment** | Vercel | Serverless deployment platform |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       Next.js Frontend                          │
│                                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐      │
│  │   Pages     │  │  Components  │  │  API Integration │      │
│  │             │  │              │  │                  │      │
│  │ /login      │  │ TaskList     │  │ fetch() + JWT    │      │
│  │ /signup     │  │ ChatWidget   │  │ React Query      │      │
│  │ /tasks      │  │ TaskForm     │  │ Error Handling   │      │
│  │ /chat       │  │ AuthGuard    │  │                  │      │
│  └─────────────┘  └──────────────┘  └──────────────────┘      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │           Authentication (JWT in localStorage)          │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/HTTPS
                              │ Authorization: Bearer <JWT>
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       FastAPI Backend                           │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐     │
│  │ Auth Routes  │  │ Task Routes  │  │  Chat Routes     │     │
│  │ /auth/login  │  │ /tasks       │  │  /chat           │     │
│  │ /auth/signup │  │              │  │                  │     │
│  └──────────────┘  └──────────────┘  └──────────────────┘     │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │         PostgreSQL (Users, Tasks, Conversations)        │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Key Design Principles:**
- **Stateless**: No session storage; JWT for auth
- **API-First**: Backend API consumed via fetch/React Query
- **Component-Based**: Reusable React components
- **Type-Safe**: TypeScript throughout
- **Responsive**: Mobile-first Tailwind CSS

---

## 🤖 Frontend Agents

These FTE (Full-Time Equivalent) AI Agents specialize in frontend development tasks:

### 1. Frontend Developer (`/frontend-developer`)
**Primary Agent for Frontend Work**

**Skills Available (3):**
- `/sp.vercel-deployer` - Deploy Next.js apps to Vercel
- `/sp.ab-testing` - A/B testing framework
- `/sp.uiux-designer` - UI/UX design patterns

**Use for:**
- React component development
- Next.js page implementation
- TypeScript integration
- Tailwind CSS styling
- API integration with backend
- Responsive design
- Performance optimization

---

### 2. UI/UX Designer (`/uiux-designer`)
**Design & User Experience Specialist**

**Skills Available (2):**
- `/sp.frontend-developer` - Implement UI designs
- `/sp.ab-testing` - Test design variations

**Use for:**
- User interface design
- Design system creation
- Component library design
- Accessibility (WCAG compliance)
- User flow design
- Wireframing
- Visual hierarchy

---

### 3. Vercel Deployer (`/vercel-deployer`)
**Vercel Platform Specialist**

**Skills Available (4):**
- `/sp.deployment-automation` - Automated deployments
- `/sp.production-checklist` - Production validation
- `/sp.frontend-developer` - Next.js optimization
- `/sp.performance-logger` - Performance monitoring

**Use for:**
- Vercel deployment configuration
- Next.js optimization (ISR, SSR, SSG)
- Edge Functions
- Performance optimization
- Core Web Vitals
- CDN caching

---

### 4. QA Engineer (`/qa-engineer`)
**Frontend Testing Specialist**

**Skills Available (3):**
- `/sp.edge-case-tester` - UI edge case testing
- `/sp.ab-testing` - A/B testing framework
- `/sp.production-checklist` - Production validation

**Use for:**
- Component testing (Jest, React Testing Library)
- E2E testing (Playwright, Cypress)
- Accessibility testing
- Performance testing
- Cross-browser testing

---

## 📁 Project Structure

```
frontend/
├── app/                      # Next.js App Router
│   ├── page.tsx              # Home page (redirects to /tasks or /login)
│   ├── layout.tsx            # Root layout with providers
│   ├── login/                # Login page
│   │   └── page.tsx
│   ├── signup/               # Signup page
│   │   └── page.tsx
│   ├── tasks/                # Tasks page (protected)
│   │   └── page.tsx
│   └── chat/                 # AI Chat page (protected)
│       └── page.tsx
├── components/               # React components
│   ├── ui/                   # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   └── ... (more UI primitives)
│   ├── TaskList.tsx          # Task list component
│   ├── TaskForm.tsx          # Task creation form
│   ├── ChatWidget.tsx        # AI chat interface (OpenAI ChatKit)
│   ├── AuthGuard.tsx         # Protected route wrapper
│   └── NavBar.tsx            # Navigation bar
├── lib/                      # Utilities and helpers
│   ├── api.ts                # API client functions
│   ├── auth.ts               # Auth utilities (JWT handling)
│   └── utils.ts              # General utilities
├── hooks/                    # Custom React hooks
│   ├── useAuth.ts            # Authentication hook
│   ├── useTasks.ts           # Tasks data fetching hook
│   └── useChat.ts            # Chat conversation hook
├── styles/                   # Global styles
│   └── globals.css           # Tailwind CSS imports
├── public/                   # Static assets
│   ├── favicon.ico
│   └── images/
├── .env.example              # Environment variables template
├── .env.local                # Local environment variables (gitignored)
├── next.config.js            # Next.js configuration
├── tailwind.config.ts        # Tailwind CSS configuration
├── tsconfig.json             # TypeScript configuration
├── package.json              # Dependencies
└── README.md                 # This file
```

---

## 🚀 Setup & Installation

### Prerequisites

- **Node.js**: 18+ (LTS recommended)
- **npm**: 9+ or **yarn**: 1.22+
- **Backend**: FastAPI backend running at `http://localhost:8000`

### Installation Steps

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Create environment file
cp .env.example .env.local

# 4. Edit .env.local with your values
# NEXT_PUBLIC_API_URL=http://localhost:8000

# 5. Start development server
npm run dev

# 6. Open browser
# Visit http://localhost:3000
```

### Environment Variables

Create `.env.local` file:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# App URL (for production)
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**⚠️ Note**: All variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

---

## 🧩 Components

### Core Components

#### 1. **TaskList** (`components/TaskList.tsx`)
Displays user's tasks with actions (complete, delete, edit).

**Props:**
```typescript
interface TaskListProps {
  tasks: Task[]
  onComplete: (taskId: string) => void
  onDelete: (taskId: string) => void
  onEdit: (taskId: string) => void
}
```

#### 2. **TaskForm** (`components/TaskForm.tsx`)
Form for creating/editing tasks.

**Props:**
```typescript
interface TaskFormProps {
  onSubmit: (task: CreateTaskDTO) => void
  initialValues?: Task
  isEditing?: boolean
}
```

#### 3. **ChatWidget** (`components/ChatWidget.tsx`)
AI chatbot interface using OpenAI ChatKit.

**Props:**
```typescript
interface ChatWidgetProps {
  conversationId?: string
  onMessage: (message: string) => void
}
```

#### 4. **AuthGuard** (`components/AuthGuard.tsx`)
HOC to protect routes requiring authentication.

**Usage:**
```typescript
export default function TasksPage() {
  return (
    <AuthGuard>
      <TaskList />
    </AuthGuard>
  )
}
```

### UI Components (shadcn/ui)

All UI primitives are in `components/ui/`:
- `Button` - Accessible button with variants
- `Input` - Form input with validation
- `Card` - Content container
- `Dialog` - Modal dialogs
- `Toast` - Notifications
- `Dropdown` - Dropdown menus
- More components as needed

---

## 📄 Pages & Routes

### Public Routes

| Route | Page | Description |
|-------|------|-------------|
| `/` | Home | Redirects to `/tasks` (if authenticated) or `/login` |
| `/login` | Login | User login form |
| `/signup` | Signup | User registration form |

### Protected Routes

| Route | Page | Description |
|-------|------|-------------|
| `/tasks` | Tasks | Traditional task management UI |
| `/chat` | Chat | AI chatbot interface |

**Protected Route Logic:**
```typescript
// app/tasks/page.tsx
export default function TasksPage() {
  const router = useRouter()
  const { user, loading } = useAuth()

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  if (loading) return <LoadingSkeleton />
  if (!user) return null

  return <TasksPageContent />
}
```

---

## 🔌 API Integration

### API Client (`lib/api.ts`)

**Base Configuration:**
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = {
  async fetch(endpoint: string, options?: RequestInit) {
    const token = localStorage.getItem('token')
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options?.headers,
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    })

    if (response.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
      throw new Error('Unauthorized')
    }

    return response
  }
}
```

### API Endpoints Used

#### Authentication
```typescript
// POST /api/auth/signup
const signup = async (data: SignupDTO) => {
  const response = await apiClient.fetch('/api/auth/signup', {
    method: 'POST',
    body: JSON.stringify(data),
  })
  return response.json()
}

// POST /api/auth/login
const login = async (data: LoginDTO) => {
  const response = await apiClient.fetch('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify(data),
  })
  const { access_token } = await response.json()
  localStorage.setItem('token', access_token)
  return access_token
}
```

#### Tasks
```typescript
// GET /api/tasks
const getTasks = async () => {
  const response = await apiClient.fetch('/api/tasks')
  return response.json()
}

// POST /api/tasks
const createTask = async (data: CreateTaskDTO) => {
  const response = await apiClient.fetch('/api/tasks', {
    method: 'POST',
    body: JSON.stringify(data),
  })
  return response.json()
}

// PATCH /api/tasks/{task_id}
const updateTask = async (taskId: string, data: UpdateTaskDTO) => {
  const response = await apiClient.fetch(`/api/tasks/${taskId}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  })
  return response.json()
}

// DELETE /api/tasks/{task_id}
const deleteTask = async (taskId: string) => {
  await apiClient.fetch(`/api/tasks/${taskId}`, {
    method: 'DELETE',
  })
}
```

#### Chat
```typescript
// POST /api/chat
const sendChatMessage = async (message: string, conversationId?: string) => {
  const response = await apiClient.fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message, conversation_id: conversationId }),
  })
  return response.json()
}

// GET /api/conversations/{conversation_id}
const getConversation = async (conversationId: string) => {
  const response = await apiClient.fetch(`/api/conversations/${conversationId}`)
  return response.json()
}
```

### React Query Integration

```typescript
// hooks/useTasks.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getTasks, createTask, updateTask, deleteTask } from '@/lib/api'

export const useTasks = () => {
  const queryClient = useQueryClient()

  const { data: tasks, isLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: getTasks,
  })

  const createMutation = useMutation({
    mutationFn: createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => updateTask(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: deleteTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  return {
    tasks,
    isLoading,
    createTask: createMutation.mutate,
    updateTask: updateMutation.mutate,
    deleteTask: deleteMutation.mutate,
  }
}
```

---

## 🔐 Authentication

### JWT Token Flow

```
┌──────────┐                          ┌──────────┐
│  User    │                          │ Backend  │
└────┬─────┘                          └────┬─────┘
     │                                     │
     │  1. Login (email, password)         │
     ├────────────────────────────────────>│
     │                                     │
     │  2. JWT Token                       │
     │<────────────────────────────────────┤
     │                                     │
     │  3. Store in localStorage           │
     │                                     │
     │  4. API Request + Auth Header       │
     ├────────────────────────────────────>│
     │    Authorization: Bearer <JWT>      │
     │                                     │
     │  5. Response                        │
     │<────────────────────────────────────┤
     │                                     │
```

### Auth Hook (`hooks/useAuth.ts`)

```typescript
export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      // Decode JWT to get user info (or fetch from /api/me)
      const decoded = jwtDecode(token)
      setUser(decoded.user)
    }
    setLoading(false)
  }, [])

  const login = async (email: string, password: string) => {
    const token = await apiClient.login({ email, password })
    const decoded = jwtDecode(token)
    setUser(decoded.user)
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
    router.push('/login')
  }

  return { user, loading, login, logout }
}
```

### Protected Route Pattern

```typescript
// components/AuthGuard.tsx
export const AuthGuard = ({ children }: { children: React.ReactNode }) => {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  if (loading) return <LoadingSpinner />
  if (!user) return null

  return <>{children}</>
}
```

---

## 🎨 Styling & Design

### Tailwind CSS Configuration

```javascript
// tailwind.config.ts
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        },
      },
    },
  },
  plugins: [],
}
```

### Design Tokens

**Colors:**
```css
/* Primary */
--primary-50: #eff6ff;
--primary-500: #3b82f6;
--primary-900: #1e3a8a;

/* Usage */
.btn-primary { @apply bg-primary-500 text-white; }
```

**Typography:**
```css
text-xs    /* 12px */
text-sm    /* 14px */
text-base  /* 16px */
text-lg    /* 18px */
text-xl    /* 20px */
text-2xl   /* 24px */
```

**Spacing:**
```css
space-1  /* 4px */
space-2  /* 8px */
space-4  /* 16px */
space-8  /* 32px */
```

### Component Variants

```typescript
// Example: Button component
<Button variant="primary">Submit</Button>
<Button variant="secondary">Cancel</Button>
<Button variant="outline">Edit</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
```

---

## 🧪 Testing

### Unit/Component Tests (Jest + React Testing Library)

```bash
# Run all tests
npm run test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage
```

**Example Component Test:**
```typescript
// __tests__/TaskList.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { TaskList } from '@/components/TaskList'

test('renders tasks correctly', () => {
  const tasks = [
    { id: '1', title: 'Buy milk', completed: false },
    { id: '2', title: 'Walk dog', completed: true },
  ]

  render(<TaskList tasks={tasks} onComplete={jest.fn()} onDelete={jest.fn()} />)

  expect(screen.getByText('Buy milk')).toBeInTheDocument()
  expect(screen.getByText('Walk dog')).toBeInTheDocument()
})

test('calls onComplete when checkbox clicked', async () => {
  const onComplete = jest.fn()
  const tasks = [{ id: '1', title: 'Buy milk', completed: false }]

  render(<TaskList tasks={tasks} onComplete={onComplete} onDelete={jest.fn()} />)

  const checkbox = screen.getByRole('checkbox')
  await userEvent.click(checkbox)

  expect(onComplete).toHaveBeenCalledWith('1')
})
```

### E2E Tests (Playwright)

```bash
# Run E2E tests
npm run test:e2e

# Open UI mode
npm run test:e2e:ui
```

**Example E2E Test:**
```typescript
// e2e/tasks.spec.ts
import { test, expect } from '@playwright/test'

test('user can create a task', async ({ page }) => {
  // Login
  await page.goto('/login')
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'password123')
  await page.click('button:has-text("Login")')

  // Create task
  await page.goto('/tasks')
  await page.fill('[placeholder="Add new task"]', 'Buy groceries')
  await page.click('button:has-text("Add")')

  // Verify
  await expect(page.locator('text=Buy groceries')).toBeVisible()
})
```

### Accessibility Tests

```typescript
// __tests__/accessibility.test.tsx
import { render } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

test('TaskList has no accessibility violations', async () => {
  const { container } = render(<TaskList tasks={[]} />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

---

## 🚀 Deployment

### Vercel Deployment

#### Method 1: GitHub Integration (Recommended)

1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import GitHub repository
4. Configure environment variables:
   - `NEXT_PUBLIC_API_URL=https://your-backend.com`
5. Deploy

#### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Production deployment
vercel --prod
```

### Environment Variables (Production)

Set in Vercel Dashboard:
```
NEXT_PUBLIC_API_URL=https://api.your-domain.com
NEXT_PUBLIC_APP_URL=https://your-domain.com
```

### Build Configuration

```javascript
// next.config.js
module.exports = {
  reactStrictMode: true,
  swcMinify: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
}
```

### Production Checklist

- [ ] Environment variables configured
- [ ] Build succeeds (`npm run build`)
- [ ] No console errors in production build
- [ ] HTTPS enabled
- [ ] CORS configured on backend
- [ ] Performance optimized (Lighthouse > 90)
- [ ] SEO metadata added
- [ ] Error tracking configured (Sentry)
- [ ] Analytics configured (Google Analytics)

---

## 📚 Resources

### Documentation
- **Root CLAUDE.md**: `../CLAUDE.md` - Project-wide guidelines
- **Backend CLAUDE.md**: `../backend/CLAUDE.md` - Backend-specific guides
- **Constitution**: `../.specify/memory/constitution.md` - Project principles
- **Skills Directory**: `../.claude/skills/` - All reusable skills
- **Agents Directory**: `../.claude/agents/` - All FTE agents

### External Docs
- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Components](https://ui.shadcn.com)
- [React Query Documentation](https://tanstack.com/query/latest)
- [OpenAI ChatKit](https://platform.openai.com/docs/chatkit)

### Scripts Reference

```bash
# Development
npm run dev              # Start dev server (http://localhost:3000)

# Building
npm run build            # Production build
npm run start            # Start production server

# Testing
npm run test             # Run unit/component tests
npm run test:watch       # Watch mode
npm run test:coverage    # Coverage report
npm run test:e2e         # E2E tests (Playwright)

# Linting & Formatting
npm run lint             # ESLint
npm run lint:fix         # Fix linting issues
npm run format           # Prettier
npm run type-check       # TypeScript type checking

# Analysis
npm run analyze          # Bundle size analysis
```

---

## 🏆 Best Practices

### Component Design
- ✅ Single Responsibility Principle
- ✅ Reusable and composable
- ✅ Typed with TypeScript
- ✅ Props interface documented
- ✅ Default props defined

### State Management
- ✅ React Query for server state
- ✅ Context API for global UI state
- ✅ Local state with useState
- ✅ Avoid prop drilling
- ✅ Memoize expensive computations

### Performance
- ✅ `next/image` for images
- ✅ Dynamic imports for code splitting
- ✅ `React.memo` for expensive components
- ✅ `useCallback`/`useMemo` where needed
- ✅ Virtualization for long lists

### Accessibility
- ✅ Semantic HTML elements
- ✅ ARIA labels and roles
- ✅ Keyboard navigation support
- ✅ Focus management
- ✅ Screen reader compatibility

---

**Frontend Development** - Powered by Reusable Intelligence 🚀

**For detailed agent and skill usage, see:**
- `../CLAUDE.md` - Root documentation
- `./CLAUDE.md` - Frontend-specific guide
- `../.claude/agents/` - FTE agent definitions
- `../.claude/skills/` - Reusable intelligence skills
