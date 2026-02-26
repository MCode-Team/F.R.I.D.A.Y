# 📝 ตัวอย่างการ Migrate จริง: C# → React + Elysia.js

**ตัวอย่าง:** User Management Module

---

## 📂 โครงสร้างไฟล์

### เดิม (C# .NET Razor Pages)

```
OldProject/
├── Models/
│   └── User.cs
├── Pages/
│   └── Users/
│       ├── Index.cshtml
│       ├── Index.cshtml.cs
│       ├── Create.cshtml
│       ├── Create.cshtml.cs
│       ├── Edit.cshtml
│       ├── Edit.cshtml.cs
│       ├── Details.cshtml
│       ├── Details.cshtml.cs
│       └── Delete.cshtml.cs
└── Data/
    └── AppDbContext.cs
```

### ใหม่ (React + Elysia.js)

```
NewProject/
├── api/                          # Elysia.js Backend
│   ├── src/
│   │   ├── routes/
│   │   │   └── users.ts          # User API routes
│   │   ├── models/
│   │   │   └── user.ts           # User type definitions
│   │   ├── services/
│   │   │   └── userService.ts    # Business logic
│   │   └── index.ts              # Main app
│   └── prisma/
│       └── schema.prisma         # Database schema
│
├── web/                          # React Frontend
│   └── src/
│       ├── pages/
│       │   └── Users/
│       │       ├── UsersList.tsx
│       │       ├── UserForm.tsx
│       │       └── UserDetail.tsx
│       ├── services/
│       │   └── userService.ts    # API client
│       └── types/
│           └── user.ts           # TypeScript types
│
└── shared/
    └── types/
        └── api.ts                # Shared types
```

---

## 🔄 ตัวอย่างการแปลงโค้ด

### 1. Model: C# → Prisma Schema

#### เดิม (Models/User.cs)

```csharp
using System;
using System.ComponentModel.DataAnnotations;

namespace OldProject.Models
{
    public class User
    {
        public int Id { get; set; }
        
        [Required]
        [StringLength(50)]
        public string Username { get; set; }
        
        [Required]
        [EmailAddress]
        public string Email { get; set; }
        
        [StringLength(100)]
        public string? FullName { get; set; }
        
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        
        public DateTime? UpdatedAt { get; set; }
        
        public bool IsActive { get; set; } = true;
    }
}
```

#### ใหม่ (prisma/schema.prisma)

```prisma
model User {
  id        Int       @id @default(autoincrement())
  username  String    @db.VarChar(50)
  email     String    @db.VarChar(255)
  fullName  String?   @db.VarChar(100)
  createdAt DateTime  @default(now())
  updatedAt DateTime? @updatedAt
  isActive  Boolean   @default(true)

  @@unique([username])
  @@unique([email])
  @@index([isActive])
  @@map("users")
}
```

**Claude Code Prompt:**
```bash
"Convert the C# User model in Models/User.cs to a Prisma schema.
Include:
- All properties with correct types
- Validation rules as Prisma constraints
- Indexes for frequently queried fields
- Map to table name 'users'"
```

---

### 2. API Route: Razor Page Handler → Elysia.js Route

#### เดิม (Pages/Users/Index.cshtml.cs)

```csharp
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using OldProject.Data;
using OldProject.Models;

namespace OldProject.Pages.Users
{
    public class IndexModel : PageModel
    {
        private readonly AppDbContext _context;
        
        public List<User> Users { get; set; }
        
        [BindProperty(SupportsGet = true)]
        public string SearchTerm { get; set; }
        
        [BindProperty(SupportsGet = true)]
        public int PageNumber { get; set; } = 1;
        
        public int PageSize { get; set; } = 10;
        public int TotalPages { get; set; }

        public IndexModel(AppDbContext context)
        {
            _context = context;
        }

        public async Task OnGetAsync()
        {
            var query = _context.Users.AsQueryable();
            
            if (!string.IsNullOrEmpty(SearchTerm))
            {
                query = query.Where(u => 
                    u.Username.Contains(SearchTerm) || 
                    u.Email.Contains(SearchTerm));
            }
            
            var totalItems = await query.CountAsync();
            TotalPages = (int)Math.Ceiling(totalItems / (double)PageSize);
            
            Users = await query
                .OrderByDescending(u => u.CreatedAt)
                .Skip((PageNumber - 1) * PageSize)
                .Take(PageSize)
                .ToListAsync();
        }
    }
}
```

#### ใหม่ (api/src/routes/users.ts)

```typescript
import { Elysia, t } from 'elysia'
import { prisma } from '../db'
import { isAuthenticated } from '../middleware/auth'

export const userRoutes = new Elysia({ prefix: '/api/users' })
  .use(isAuthenticated)
  
  // GET /api/users - List users with pagination and search
  .get('/', async ({ query }) => {
    const { searchTerm, page = 1, limit = 10 } = query
    const skip = (page - 1) * limit

    const where = searchTerm
      ? {
          OR: [
            { username: { contains: searchTerm } },
            { email: { contains: searchTerm } }
          ]
        }
      : {}

    const [users, total] = await Promise.all([
      prisma.user.findMany({
        where,
        orderBy: { createdAt: 'desc' },
        skip,
        take: limit,
        select: {
          id: true,
          username: true,
          email: true,
          fullName: true,
          isActive: true,
          createdAt: true
        }
      }),
      prisma.user.count({ where })
    ])

    return {
      data: users,
      pagination: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit)
      }
    }
  }, {
    query: t.Object({
      searchTerm: t.Optional(t.String()),
      page: t.Optional(t.Number({ minimum: 1 })),
      limit: t.Optional(t.Number({ minimum: 1, maximum: 100 }))
    }),
    response: t.Object({
      data: t.Array(t.Object({
        id: t.Number(),
        username: t.String(),
        email: t.String(),
        fullName: t.Nullable(t.String()),
        isActive: t.Boolean(),
        createdAt: t.Date()
      })),
      pagination: t.Object({
        page: t.Number(),
        limit: t.Number(),
        total: t.Number(),
        totalPages: t.Number()
      })
    }),
    detail: {
      summary: 'List users',
      tags: ['Users']
    }
  })

  // GET /api/users/:id - Get user by ID
  .get('/:id', async ({ params, set }) => {
    const user = await prisma.user.findUnique({
      where: { id: params.id }
    })

    if (!user) {
      set.status = 404
      throw new Error('User not found')
    }

    return user
  }, {
    params: t.Object({
      id: t.Number()
    }),
    response: t.Object({
      id: t.Number(),
      username: t.String(),
      email: t.String(),
      fullName: t.Nullable(t.String()),
      isActive: t.Boolean(),
      createdAt: t.Date(),
      updatedAt: t.Nullable(t.Date())
    }),
    detail: {
      summary: 'Get user by ID',
      tags: ['Users']
    }
  })

  // POST /api/users - Create new user
  .post('/', async ({ body, set }) => {
    // Check if username or email already exists
    const existing = await prisma.user.findFirst({
      where: {
        OR: [
          { username: body.username },
          { email: body.email }
        ]
      }
    })

    if (existing) {
      set.status = 400
      throw new Error('Username or email already exists')
    }

    const user = await prisma.user.create({
      data: body
    })

    set.status = 201
    return user
  }, {
    body: t.Object({
      username: t.String({ minLength: 3, maxLength: 50 }),
      email: t.String({ format: 'email' }),
      fullName: t.Optional(t.String({ maxLength: 100 }))
    }),
    response: t.Object({
      id: t.Number(),
      username: t.String(),
      email: t.String(),
      fullName: t.Nullable(t.String()),
      isActive: t.Boolean(),
      createdAt: t.Date()
    }),
    detail: {
      summary: 'Create new user',
      tags: ['Users']
    }
  })

  // PUT /api/users/:id - Update user
  .put('/:id', async ({ params, body, set }) => {
    const existing = await prisma.user.findUnique({
      where: { id: params.id }
    })

    if (!existing) {
      set.status = 404
      throw new Error('User not found')
    }

    // Check if new username/email conflicts with other users
    if (body.username || body.email) {
      const conflict = await prisma.user.findFirst({
        where: {
          AND: [
            { id: { not: params.id } },
            {
              OR: [
                ...(body.username ? [{ username: body.username }] : []),
                ...(body.email ? [{ email: body.email }] : [])
              ]
            }
          ]
        }
      })

      if (conflict) {
        set.status = 400
        throw new Error('Username or email already in use')
      }
    }

    const user = await prisma.user.update({
      where: { id: params.id },
      data: body
    })

    return user
  }, {
    params: t.Object({
      id: t.Number()
    }),
    body: t.Object({
      username: t.Optional(t.String({ minLength: 3, maxLength: 50 })),
      email: t.Optional(t.String({ format: 'email' })),
      fullName: t.Optional(t.String({ maxLength: 100 })),
      isActive: t.Optional(t.Boolean())
    }),
    response: t.Object({
      id: t.Number(),
      username: t.String(),
      email: t.String(),
      fullName: t.Nullable(t.String()),
      isActive: t.Boolean(),
      createdAt: t.Date(),
      updatedAt: t.Nullable(t.Date())
    }),
    detail: {
      summary: 'Update user',
      tags: ['Users']
    }
  })

  // DELETE /api/users/:id - Delete user
  .delete('/:id', async ({ params, set }) => {
    const existing = await prisma.user.findUnique({
      where: { id: params.id }
    })

    if (!existing) {
      set.status = 404
      throw new Error('User not found')
    }

    await prisma.user.delete({
      where: { id: params.id }
    })

    set.status = 204
    return { message: 'User deleted successfully' }
  }, {
    params: t.Object({
      id: t.Number()
    }),
    response: t.Object({
      message: t.String()
    }),
    detail: {
      summary: 'Delete user',
      tags: ['Users']
    }
  })
```

**Claude Code Prompt:**
```bash
"Convert the Razor Page handler in Pages/Users/Index.cshtml.cs to an 
Elysia.js route. Include:
- All CRUD operations (GET, POST, PUT, DELETE)
- TypeBox validation schemas
- Error handling with proper HTTP status codes
- Pagination and search support
- Swagger documentation
- JWT authentication middleware"
```

---

### 3. Frontend: Razor Page → React Component

#### เดิม (Pages/Users/Index.cshtml)

```cshtml
@page
@model IndexModel
@{
    ViewData["Title"] = "Users";
}

<div class="container">
    <h1>Users</h1>
    
    <form method="get" class="mb-3">
        <div class="row">
            <div class="col-md-6">
                <input type="text" 
                       name="searchTerm" 
                       value="@Model.SearchTerm" 
                       placeholder="Search users..." 
                       class="form-control" />
            </div>
            <div class="col-md-2">
                <button type="submit" class="btn btn-primary">Search</button>
            </div>
        </div>
    </form>
    
    @if (TempData["SuccessMessage"] != null)
    {
        <div class="alert alert-success">
            @TempData["SuccessMessage"]
        </div>
    }
    
    <a href="/Users/Create" class="btn btn-success mb-3">Create New</a>
    
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Full Name</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            @foreach (var user in Model.Users)
            {
                <tr>
                    <td>@user.Username</td>
                    <td>@user.Email</td>
                    <td>@user.FullName</td>
                    <td>
                        @if (user.IsActive)
                        {
                            <span class="badge bg-success">Active</span>
                        }
                        else
                        {
                            <span class="badge bg-secondary">Inactive</span>
                        }
                    </td>
                    <td>@user.CreatedAt.ToString("yyyy-MM-dd")</td>
                    <td>
                        <a href="/Users/Details/@user.Id" class="btn btn-sm btn-info">Details</a>
                        <a href="/Users/Edit/@user.Id" class="btn btn-sm btn-warning">Edit</a>
                        <a href="/Users/Delete/@user.Id" class="btn btn-sm btn-danger">Delete</a>
                    </td>
                </tr>
            }
        </tbody>
    </table>
    
    @if (Model.TotalPages > 1)
    {
        <nav>
            <ul class="pagination">
                @for (int i = 1; i <= Model.TotalPages; i++)
                {
                    <li class="page-item @(i == Model.PageNumber ? "active" : "")">
                        <a class="page-link" 
                           href="?pageNumber=@i&searchTerm=@Model.SearchTerm">
                            @i
                        </a>
                    </li>
                }
            </ul>
        </nav>
    }
</div>
```

#### ใหม่ (web/src/pages/Users/UsersList.tsx)

```tsx
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link, useSearchParams } from 'react-router-dom'
import { userService } from '@/services/userService'
import type { User } from '@/types/user'

export function UsersList() {
  const [searchParams, setSearchParams] = useSearchParams()
  const searchTerm = searchParams.get('search') || ''
  const page = parseInt(searchParams.get('page') || '1', 10)
  const [localSearch, setLocalSearch] = useState(searchTerm)

  const { data, isLoading, error } = useQuery({
    queryKey: ['users', { searchTerm, page }],
    queryFn: () => userService.getAll({ searchTerm, page, limit: 10 })
  })

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setSearchParams({ search: localSearch, page: '1' })
  }

  const handlePageChange = (newPage: number) => {
    setSearchParams({ 
      search: searchTerm, 
      page: newPage.toString() 
    })
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          Error loading users. Please try again.
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Users</h1>
        <Link
          to="/users/create"
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
        >
          Create New
        </Link>
      </div>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={localSearch}
            onChange={(e) => setLocalSearch(e.target.value)}
            placeholder="Search users..."
            className="flex-1 px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded"
          >
            Search
          </button>
        </div>
      </form>

      {/* Users Table */}
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <table className="min-w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Username
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Email
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Full Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Created
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data?.data.map((user: User) => (
              <tr key={user.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">
                    {user.username}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-500">{user.email}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">
                    {user.fullName || '-'}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      user.isActive
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {user.isActive ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(user.createdAt).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <Link
                    to={`/users/${user.id}`}
                    className="text-blue-600 hover:text-blue-900"
                  >
                    Details
                  </Link>
                  <Link
                    to={`/users/${user.id}/edit`}
                    className="text-yellow-600 hover:text-yellow-900"
                  >
                    Edit
                  </Link>
                  <button
                    onClick={() => handleDelete(user.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {data && data.pagination.totalPages > 1 && (
        <div className="mt-6 flex justify-center">
          <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
            {Array.from({ length: data.pagination.totalPages }, (_, i) => i + 1).map(
              (pageNum) => (
                <button
                  key={pageNum}
                  onClick={() => handlePageChange(pageNum)}
                  className={`relative inline-flex items-center px-4 py-2 border text-sm font-medium ${
                    pageNum === page
                      ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                      : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                  }`}
                >
                  {pageNum}
                </button>
              )
            )}
          </nav>
        </div>
      )}
    </div>
  )
}

async function handleDelete(userId: number) {
  if (window.confirm('Are you sure you want to delete this user?')) {
    try {
      await userService.delete(userId)
      // Trigger refetch
      window.location.reload()
    } catch (error) {
      alert('Failed to delete user')
    }
  }
}
```

**Claude Cowork Prompt:**
```bash
"Convert the Razor Page at Pages/Users/Index.cshtml to a React component.
Include:
- TypeScript types
- React Query for data fetching
- React Router for navigation
- TailwindCSS for styling
- Search functionality
- Pagination
- Loading and error states
- Delete confirmation dialog"
```

---

### 4. Service Layer: API Client

#### ใหม่ (web/src/services/userService.ts)

```typescript
import axios from 'axios'
import type { User, CreateUserData, UpdateUserData } from '@/types/user'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export interface GetUsersParams {
  searchTerm?: string
  page?: number
  limit?: number
}

export interface GetUsersResponse {
  data: User[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
}

export const userService = {
  async getAll(params: GetUsersParams = {}): Promise<GetUsersResponse> {
    const response = await api.get<GetUsersResponse>('/api/users', { params })
    return response.data
  },

  async getById(id: number): Promise<User> {
    const response = await api.get<User>(`/api/users/${id}`)
    return response.data
  },

  async create(data: CreateUserData): Promise<User> {
    const response = await api.post<User>('/api/users', data)
    return response.data
  },

  async update(id: number, data: UpdateUserData): Promise<User> {
    const response = await api.put<User>(`/api/users/${id}`, data)
    return response.data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/api/users/${id}`)
  }
}
```

**Claude Code Prompt:**
```bash
"Create a TypeScript service layer for the User API. Include:
- Axios client with interceptors
- All CRUD methods
- TypeScript types
- Error handling
- Authentication token injection"
```

---

## 🧪 ตัวอย่าง Tests

### API Route Test (Vitest)

```typescript
// api/src/routes/__tests__/users.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'bun:test'
import { Elysia } from 'elysia'
import { userRoutes } from '../users'

describe('User Routes', () => {
  let app: Elysia

  beforeAll(() => {
    app = new Elysia().use(userRoutes)
  })

  describe('GET /api/users', () => {
    it('should return list of users', async () => {
      const response = await app
        .handle(new Request('http://localhost/api/users'))
        .then((res) => res.json())

      expect(response).toHaveProperty('data')
      expect(response).toHaveProperty('pagination')
      expect(Array.isArray(response.data)).toBe(true)
    })

    it('should support search', async () => {
      const response = await app
        .handle(new Request('http://localhost/api/users?searchTerm=john'))
        .then((res) => res.json())

      expect(response.data.every((user: any) => 
        user.username.includes('john') || user.email.includes('john')
      )).toBe(true)
    })

    it('should support pagination', async () => {
      const response = await app
        .handle(new Request('http://localhost/api/users?page=2&limit=5'))
        .then((res) => res.json())

      expect(response.pagination.page).toBe(2)
      expect(response.pagination.limit).toBe(5)
    })
  })

  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const newUser = {
        username: 'testuser',
        email: 'test@example.com',
        fullName: 'Test User'
      }

      const response = await app
        .handle(new Request('http://localhost/api/users', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newUser)
        }))
        .then((res) => res.json())

      expect(response.username).toBe(newUser.username)
      expect(response.email).toBe(newUser.email)
    })

    it('should validate required fields', async () => {
      const response = await app
        .handle(new Request('http://localhost/api/users', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({})
        }))

      expect(response.status).toBe(400)
    })
  })
})
```

**Claude Code Prompt:**
```bash
"Generate comprehensive Vitest tests for the user routes in 
api/src/routes/users.ts. Include:
- Unit tests for all CRUD operations
- Validation tests
- Error handling tests
- Authentication tests
- Edge cases"
```

---

## 📊 ตัวอย่าง Migration Tracking

### Progress Dashboard

```markdown
# Migration Progress Report

**Generated:** 2026-02-27 00:55:00

## Overall Progress

- **Total Files:** 45
- **Completed:** 15 (33%)
- **In Progress:** 8 (18%)
- **Not Started:** 22 (49%)

## By Category

### Models (10 files)
- [x] User.cs → Prisma schema
- [x] Role.cs → Prisma schema
- [ ] Permission.cs → Prisma schema
- [ ] ... (7 more)

### API Routes (15 files)
- [x] Users/Index.cshtml.cs → routes/users.ts
- [x] Roles/Index.cshtml.cs → routes/roles.ts
- [ ] ... (13 more)

### Frontend Components (20 files)
- [x] Users/Index.cshtml → UsersList.tsx
- [ ] Users/Create.cshtml → UserForm.tsx
- [ ] ... (18 more)

## Critical Path

1. ⏳ Authentication system (In Progress)
2. 🔴 User management (Blocked - waiting for auth)
3. ⚪ Role management (Not Started)
4. ⚪ Permission system (Not Started)

## Blockers

- 🔴 Waiting for JWT secret key from DevOps
- 🟡 Need clarification on role-permission mapping

## Next Actions

1. Complete authentication middleware
2. Finish User CRUD operations
3. Start Role management migration
```

**Claude Cowork Prompt:**
```bash
"Scan the migration project and generate a progress dashboard showing:
- Total files to migrate
- Completed migrations
- In progress items
- Blocked items
- Percentage complete
- Critical path items
- Current blockers
- Next actions

Update this report every time we complete a migration task."
```

---

## ✅ Checklist สำหรับ Migration Task นี้

### Before Starting
- [ ] Read original C# code
- [ ] Understand business logic
- [ ] Identify dependencies
- [ ] Plan API contracts
- [ ] Create feature branch

### During Migration
- [ ] Create Prisma schema
- [ ] Implement Elysia.js routes
- [ ] Add TypeBox validation
- [ ] Write API tests
- [ ] Create React components
- [ ] Implement service layer
- [ ] Add error handling
- [ ] Test integration

### After Migration
- [ ] Update documentation
- [ ] Run full test suite
- [ ] Code review
- [ ] Deploy to staging
- [ ] UAT testing
- [ ] Deploy to production

---

**หมายเหตุ:** นี่เป็นตัวอย่างเบื้องต้น สามารถปรับแต่งตามความต้องการเฉพาะของโปรเจคได้

**Happy Coding! 🚀**
