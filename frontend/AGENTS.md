# Frontend Agent Guide - Linea Supply

## Overview

**Brand:** Linea Supply - Premium minimal e-commerce with monochrome design  
**Purpose:** React TypeScript frontend for the e-commerce demo  
**Stack:** React 18, TypeScript, Vite, Chakra UI  
**Design System:** Modular theme with semantic tokens (sand/ink/charcoal colors, Inter font)  
**Architecture:** Component-based with Context API for state management

## Cursor / terminal workflow

From the **repository root**, use **`just`** (see root [AGENTS.md](../AGENTS.md) and [justfile](../justfile)):

- **Lint:** `just lint`.
- **Build / types:** `just build`.
- **Format:** `just format`.
- **Full CI:** `just ci`.

## Essential Commands

**Development:**

- `npm run dev` - Start development server (localhost:3001)
- `npm install` - Install dependencies
- `npm run preview` - Preview production build

**Quality Checks:**

- From repo root: `just lint`, `just build`, `just format`, `just ci`

## TypeScript Standards

### Strict Configuration Required

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,
    "noUncheckedIndexedAccess": true
  }
}
```

### Type Definitions

```typescript
// Domain Types
export interface Product {
  readonly id: string
  readonly name: string
  readonly price: number
  readonly category: string
  readonly description?: string
  readonly imageUrl?: string
  readonly inStock: boolean
}

export interface User {
  readonly id: string
  readonly email: string
  readonly firstName: string
  readonly lastName: string
  readonly createdAt: string
}

// Component Props
export interface ProductCardProps {
  readonly product: Product
  readonly onAddToCart: (productId: string) => void
  readonly isLoading?: boolean
}

// API Response Types
export interface ApiResponse<T> {
  readonly data: T
  readonly message?: string
}

export interface ApiError {
  readonly error: string
  readonly code: string
}
```

## Directory Structure

```
frontend/src/
├── components/          # Reusable UI components
│   └── ProductCard/
│       └── ProductCard.tsx
├── pages/               # Page-level components
├── hooks/               # Custom React hooks
├── context/             # React Context providers
├── api/                 # API client and types
├── types/               # TypeScript type definitions
└── utils/               # Helper functions
```

## Performance Best Practices

- **Lazy Loading:** Use `React.lazy()` for code splitting
- **Memoization:** Use `React.memo()`, `useMemo()`, `useCallback()` judiciously
- **Bundle Analysis:** Run `npm run build` and analyze bundle size
- **Image Optimization:** Use WebP format with fallbacks
- **API Optimization:** Implement request caching and pagination
