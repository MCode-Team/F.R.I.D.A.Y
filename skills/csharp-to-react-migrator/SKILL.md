---
name: csharp-to-react-migrator
description: Migrates C# ASP.NET Core Razor Pages projects to React + Bun.js + Elysia.js stack. Use when the user wants to convert C# models to Prisma schemas, Razor Pages to React components, or C# handlers to Elysia.js routes. Don't use for Vue, Angular, or non-Razor Pages projects.
---

# C# to React + Elysia.js Migration Skill

## Overview

This skill automates the migration of C# ASP.NET Core Razor Pages projects to a modern React + Bun.js + Elysia.js stack.

**Migration Flow:**
```
C# Model → Prisma Schema
C# Handler → Elysia.js Route
Razor Page → React Component
```

## Prerequisites

Before starting migration:

1. **Read the project structure** - Identify all .cs, .cshtml files
2. **Check dependencies** - Read .csproj for NuGet packages
3. **Map the migration scope** - See references/file-mapping-template.md

## Step-by-Step Migration Process

### Phase 1: Project Setup

**Step 1.1: Create New Project Structure**

Run the setup script:
```bash
python scripts/setup-project.py --name <project-name>
```

This creates:
```
<project-name>/
├── api/          (Elysia.js backend)
│   ├── src/
│   ├── prisma/
│   └── package.json
├── web/          (React frontend)
│   ├── src/
│   └── package.json
└── shared/       (Shared TypeScript types)
```

**Step 1.2: Initialize Dependencies**

The script automatically runs:
- `bun init` for API project
- `bun create vite` for React project
- Installs required packages (see references/dependencies.md)

### Phase 2: Data Models Migration

**Step 2.1: Convert C# Models to Prisma Schema**

For each C# model file:
```bash
python scripts/convert-model.py <path-to-model.cs> --output api/prisma/schema.prisma
```

The script:
1. Parses C# properties and types
2. Maps C# types to Prisma types (see references/type-mapping.md)
3. Generates Prisma schema with proper relations
4. Adds indexes for frequently queried fields

**Manual Review Required:**
- Check complex relationships (many-to-many)
- Validate enum mappings
- Confirm default values

**Step 2.2: Run Prisma Migration**

```bash
cd api
bunx prisma migrate dev --name init
```

If errors occur, see references/prisma-errors.md.

### Phase 3: API Routes Migration

**Step 3.1: Convert C# Handlers to Elysia Routes**

For each Razor Page handler (.cshtml.cs):
```bash
python scripts/convert-handler.py <path-to-handler.cs> --output api/src/routes/
```

The script generates:
- Elysia.js route with proper HTTP methods
- TypeBox validation schemas
- Error handling middleware
- Swagger documentation

**Manual Tasks:**
- Inject authentication middleware (see references/auth-setup.md)
- Add business logic from C# services
- Implement complex validation rules

**Step 3.2: Generate TypeBox Schemas**

For complex validation, use the schema generator:
```bash
python scripts/generate-schema.py <csharp-class> --output api/src/schemas/
```

### Phase 4: Frontend Migration

**Step 4.1: Convert Razor Pages to React Components**

For each Razor Page (.cshtml):
```bash
python scripts/convert-razor.py <path-to-page.cshtml> --output web/src/pages/
```

The script:
1. Extracts server-side logic to API calls
2. Converts Razor syntax to JSX
3. Adds React Query hooks for data fetching
4. Implements form validation with React Hook Form
5. Applies TailwindCSS classes

**Manual Tasks:**
- Review state management approach
- Add error boundaries
- Implement loading states
- Handle client-side routing

**Step 4.2: Create Service Layer**

Generate API client services:
```bash
python scripts/generate-service.py --api-url http://localhost:3000
```

This creates TypeScript services for all API endpoints.

**Step 4.3: Setup React Router**

Map old routes to new routes (see references/route-mapping.md):
```typescript
// web/src/router.tsx
import { UsersList } from './pages/Users/UsersList'
import { UserForm } from './pages/Users/UserForm'

export const routes = [
  { path: '/users', element: <UsersList /> },
  { path: '/users/create', element: <UserForm /> },
  { path: '/users/:id/edit', element: <UserForm /> },
]
```

### Phase 5: Testing & Validation

**Step 5.1: Generate API Tests**

```bash
python scripts/generate-api-tests.py --output api/src/__tests__/
```

Runs unit tests for all routes:
```bash
cd api && bun test
```

**Step 5.2: Generate Component Tests**

```bash
python scripts/generate-component-tests.py --output web/src/__tests__/
```

Runs React component tests:
```bash
cd web && bun test
```

**Step 5.3: Run Integration Tests**

Test the full stack:
```bash
# Start API server
cd api && bun run dev

# Start React dev server
cd web && bun run dev

# Run E2E tests (if configured)
bun run test:e2e
```

### Phase 6: Documentation

**Step 6.1: Generate API Documentation**

Elysia.js auto-generates Swagger docs at:
```
http://localhost:3000/swagger
```

**Step 6.2: Create Component Storybook**

For React components:
```bash
cd web
bunx storybook init
bun run storybook
```

## Error Handling

### Common Migration Issues

**Issue 1: Complex C# LINQ Queries**
- Cannot auto-convert complex LINQ
- Manual translation required
- See references/linq-to-prisma.md for patterns

**Issue 2: Session State Management**
- C# uses server-side sessions
- Migrate to JWT + React Context
- See references/auth-migration.md

**Issue 3: ViewData/ViewBag**
- Server-side data passing
- Replace with React props or React Query
- See references/state-migration.md

**Issue 4: Partial Views**
- Reusable Razor components
- Convert to React components
- See references/component-migration.md

### Script Failure Recovery

If any script fails:
1. Check error message in console
2. See references/error-codes.md
3. Fix the C# source file manually
4. Re-run the script with --verbose flag
5. If persistent, use manual migration (see assets/manual-migration-checklist.md)

## Progressive Disclosure

**Only load references when needed:**

- For type mappings: Read references/type-mapping.md
- For Prisma errors: Read references/prisma-errors.md
- For auth setup: Read references/auth-setup.md
- For route mapping: Read references/route-mapping.md
- For component patterns: Read references/react-patterns.md

## Output Structure

After migration, the project structure is:

```
project/
├── api/
│   ├── src/
│   │   ├── routes/         # Elysia.js routes
│   │   ├── services/       # Business logic
│   │   ├── schemas/        # TypeBox validation
│   │   └── index.ts        # Main app
│   ├── prisma/
│   │   └── schema.prisma   # Database schema
│   └── tests/
│
├── web/
│   ├── src/
│   │   ├── pages/          # React pages
│   │   ├── components/     # Reusable components
│   │   ├── services/       # API clients
│   │   ├── hooks/          # Custom hooks
│   │   └── types/          # TypeScript types
│   └── tests/
│
└── shared/
    └── types/              # Shared API types
```

## Validation Checklist

After migration, verify:

- [ ] All models migrated to Prisma
- [ ] All handlers converted to Elysia routes
- [ ] All Razor pages converted to React
- [ ] API tests passing (>80% coverage)
- [ ] Component tests passing (>80% coverage)
- [ ] No TypeScript errors
- [ ] API documentation generated
- [ ] Authentication working
- [ ] Database migrations successful
- [ ] E2E tests passing (if configured)

## Notes

- **Don't migrate everything at once** - Use Strangler Pattern
- **Run both systems in parallel** - Test incrementally
- **Keep the C# project** - Reference during migration
- **Document edge cases** - Add to references/ as discovered
- **Test frequently** - Run tests after each module migration

## Support

If stuck:
1. Check references/ directory for specific topics
2. See assets/ for templates and examples
3. Review migration-examples.md in the main project docs
4. Consult the architecture document for design decisions
