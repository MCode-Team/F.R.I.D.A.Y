# 🤖 คู่มือใช้ Claude Code & Cowork สำหรับ Migration Project

**สร้างเมื่อ:** 27 กุมภาพันธ์ 2569  
**โดย:** จาวิส

---

## 📋 สรุป Use Cases สำหรับ Migration นี้

### 🔧 Claude Code (Terminal-based AI Coding Agent)

#### ใช้ทำอะไรได้บ้าง?

✅ **Code Analysis & Understanding**
- อ่านและวิเคราะห์ C# Razor Pages codebase ทั้งหมด
- เข้าใจ business logic และ data flow
- ระบุ dependencies และ potential issues

✅ **Code Translation & Migration**
- แปลง C# models → Prisma schema
- แปลง Razor syntax (.cshtml) → React JSX/TSX
- แปลง C# controllers → Elysia.js routes
- แปลง business logic C# → TypeScript

✅ **API Development**
- สร้าง REST API endpoints ใหม่
- Generate TypeScript types จาก C# models
- Implement validation ด้วย TypeBox
- Setup Swagger documentation

✅ **Testing & Quality**
- สร้าง unit tests สำหรับ React components
- Generate API integration tests
- Setup E2E testing scenarios
- Code coverage reporting

✅ **Git & DevOps**
- จัดการ git branches และ PRs
- Setup CI/CD pipelines
- Create deployment scripts

#### 🎯 Best Practices สำหรับ Migration

```bash
# 1. ให้ Claude Code วิเคราะห์โปรเจคเก่าก่อน
claude-code "Analyze the C# Razor Pages project structure in ../old-project/
and create a migration plan"

# 2. ให้สร้าง initial setup
claude-code "Setup a new Elysia.js project with TypeScript, 
Prisma, JWT auth, and Swagger"

# 3. ให้ migrate model ทีละกลุ่ม
claude-code "Migrate all models in Models/User.cs to Prisma schema
with proper relations and indexes"

# 4. ให้สร้าง API routes
claude-code "Convert Pages/Users/*.cshtml.cs handlers to 
Elysia.js routes with TypeBox validation"

# 5. ให้สร้าง React components
claude-code "Convert Pages/Users/Index.cshtml to React component
with React Query for data fetching"
```

---

### 🤝 Claude Cowork (Desktop AI Agent)

#### ใช้ทำอะไรได้บ้าง?

✅ **Autonomous Task Execution**
- ทำงาน batch migration หลายไฟล์พร้อมกัน
- Parallel processing ของ sub-tasks
- Coordinate ระหว่าง frontend/backend teams

✅ **File Management**
- อ่าน/เขียนไฟล์ทั้งโปรเจค
- จัดระเบียบโครงสร้างโฟลเดอร์
- Batch rename/move files
- Track migration progress

✅ **Documentation & Reporting**
- สร้าง API documentation อัตโนมัติ
- Generate migration checklists
- Create component storybooks
- Build architecture diagrams

✅ **Multi-file Operations**
- Batch convert 50+ .cshtml files
- Generate TypeScript types จาก C# models
- Create migration scripts
- Setup configuration files

#### 🎯 Best Practices สำหรับ Migration

```bash
# 1. ให้ Cowork สร้าง project structure
"Create a new project structure for React + Elysia.js migration:
- /api (Elysia.js backend)
- /web (React frontend)
- /shared (shared types)
- /docs (documentation)
- /scripts (migration scripts)"

# 2. ให้วิเคราะห์และสร้าง migration checklist
"Analyze all .cshtml files in the old project and create a 
migration checklist with:
- File path
- Dependencies
- Complexity score
- Estimated time
- Priority"

# 3. ให้ batch convert ไฟล์
"Convert all .cshtml files in Pages/Users/ to React components.
For each file:
- Create corresponding .tsx file
- Extract inline styles to Tailwind classes
- Convert server-side logic to API calls
- Add React Query hooks"

# 4. ให้สร้าง documentation
"Generate comprehensive API documentation for all Elysia.js routes
including:
- Endpoint description
- Request/response schemas
- Example requests
- Error codes"

# 5. ให้สร้าง progress tracking
"Create a migration tracking dashboard that shows:
- Total files to migrate
- Completed migrations
- In progress
- Blocked/Issues
- Overall percentage"
```

---

## 💡 ตัวอย่างการใช้จริง

### Scenario 1: Migrate User Management Module

#### ขั้นตอนที่ 1: Analysis (ใช้ Claude Code)

```bash
cd /path/to/old-project
claude-code

# Prompt:
"Analyze the User management module in this C# project:
1. List all related files (models, controllers, views)
2. Identify business logic and validation rules
3. Map out data flow and dependencies
4. Estimate migration complexity

Create a detailed migration plan."
```

#### ขั้นตอนที่ 2: Setup (ใช้ Claude Cowork)

```bash
# Prompt:
"Based on the analysis, setup the new structure:
1. Create Prisma schema for User model
2. Create Elysia.js routes with TypeBox validation
3. Create React components for User CRUD
4. Setup API client with React Query
5. Create unit tests for all components"
```

#### ขั้นตอนที่ 3: Implementation (ใช้ทั้งสอง)

```bash
# Claude Code - สร้าง API
"Implement the following Elysia.js routes based on the C# handlers:
- GET /api/users - List all users
- GET /api/users/:id - Get user by ID
- POST /api/users - Create user
- PUT /api/users/:id - Update user
- DELETE /api/users/:id - Delete user

Include:
- TypeBox validation schemas
- Error handling
- JWT authentication
- Swagger documentation"

# Claude Cowork - สร้าง Frontend
"Create React components for User management:
1. UsersList.tsx - Display all users in a table
2. UserForm.tsx - Create/Edit user form
3. UserDetail.tsx - View user details
4. userService.ts - API client with React Query

Use:
- React Hook Form for form validation
- Zod for schema validation
- TailwindCSS for styling
- React Query for data fetching"
```

---

## 🎯 การตัดสินใจ: เลือกใช้อะไรเมื่อไหร่?

### ใช้ Claude Code เมื่อ:

✅ ต้องการ **interactive coding session**
✅ ต้องการ **run terminal commands** (npm, git, etc.)
✅ ต้องการ **debug หรือ troubleshoot**
✅ ต้องการ **ทำงานกับ git** (commit, push, PR)
✅ ต้องการ **test และ validate** code
✅ ต้องการ **setup development environment**

### ใช้ Claude Cowork เมื่อ:

✅ ต้องการ **batch process หลายไฟล์**
✅ ต้องการ **autonomous task execution**
✅ ต้องการ **สร้าง documentation**
✅ ต้องการ **coordinate หลาย tasks พร้อมกัน**
✅ ต้องการ **file management และ organization**
✅ ต้องการ **generate reports และ tracking**

### ใช้ทั้งสองร่วมกันเมื่อ:

✅ **Large-scale migration** (100+ files)
✅ **Complex business logic** ที่ต้อง analyze และ implement
✅ **Parallel work streams** (frontend + backend พร้อมกัน)
✅ **Quality assurance** (implement + test + document)

---

## 📊 ตัวอย่าง Workflow จริง

### Migration Workflow สำหรับ 1 Feature Module

```
┌─────────────────────────────────────────────┐
│   Phase 1: Analysis (Claude Code)          │
│   - Analyze C# code                        │
│   - Identify dependencies                  │
│   - Create migration plan                  │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│   Phase 2: Setup (Claude Cowork)           │
│   - Create project structure               │
│   - Setup Prisma schema                    │
│   - Generate initial files                 │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│   Phase 3: Implementation (Both)           │
│   ┌──────────────┐    ┌──────────────┐     │
│   │ Backend API  │    │  Frontend    │     │
│   │ (Claude Code)│    │ (Cowork)     │     │
│   └──────────────┘    └──────────────┘     │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│   Phase 4: Testing (Claude Code)           │
│   - Write unit tests                       │
│   - Write integration tests                │
│   - Setup E2E tests                        │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│   Phase 5: Documentation (Cowork)          │
│   - Generate API docs                      │
│   - Create component stories               │
│   - Write migration report                 │
└─────────────────────────────────────────────┘
```

---

## 🚀 Quick Start Template

### สร้างไฟล์ Prompt Templates สำหรับ Migration

```markdown
# /Users/mcode/clawd/prompts/migration-templates.md

## Template 1: Analyze C# Model

```
Analyze the C# model in {FILE_PATH} and:
1. Extract all properties and their types
2. Identify relationships with other models
3. List validation attributes
4. Suggest equivalent Prisma schema
5. Note any business logic embedded in the model
```

## Template 2: Convert Razor Page to React

```
Convert the Razor Page at {FILE_PATH} to a React component:
1. Extract server-side logic to API calls
2. Convert Razor syntax to JSX
3. Use React Query for data fetching
4. Add form validation with React Hook Form
5. Style with TailwindCSS
6. Add error handling and loading states
```

## Template 3: Generate Elysia.js Route

```
Create an Elysia.js route based on the C# handler at {FILE_PATH}:
1. Convert C# method to TypeScript
2. Add TypeBox validation schemas
3. Implement error handling
4. Add Swagger documentation
5. Include authentication middleware
```

## Template 4: Batch Convert Files

```
Batch convert all files in {DIRECTORY}:
For each .cshtml file:
1. Create corresponding React component
2. Extract styles to Tailwind
3. Convert logic to API calls
4. Add TypeScript types
5. Create unit test file

Generate a progress report showing:
- Files processed
- Errors encountered
- Warnings or notes
```

## Template 5: Create Migration Checklist

```
Analyze the entire C# project and create a migration checklist:
1. List all files to migrate
2. Group by feature/module
3. Assign priority (High/Medium/Low)
4. Estimate effort (hours)
5. Identify dependencies
6. Suggest migration order

Output as a markdown table with checkboxes.
```

## Template 6: Generate API Documentation

```
Generate comprehensive API documentation for {ROUTE_FILE}:
1. Endpoint description
2. HTTP method and path
3. Request body schema (TypeBox)
4. Response schema (TypeBox)
5. Authentication requirements
6. Example requests (curl + JavaScript)
7. Error responses
8. Rate limiting info

Format as OpenAPI/Swagger specification.
```

## Template 7: Create Test Suite

```
Create a comprehensive test suite for {COMPONENT_FILE}:
1. Unit tests with Vitest
   - Test all props
   - Test user interactions
   - Test edge cases
2. Integration tests
   - Test API calls (mocked)
   - Test data flow
3. E2E test scenario
   - User journey
   - Expected outcomes

Include test coverage report.
```

## Template 8: Setup CI/CD Pipeline

```
Create a GitHub Actions workflow for the migration project:
1. Run on pull requests
2. Steps:
   - Install dependencies
   - Run linter
   - Run type checker
   - Run unit tests
   - Run integration tests
   - Build project
   - Run E2E tests
3. Deploy to staging on main branch
4. Include caching strategies
5. Add Slack notifications
```

## Template 9: Database Migration Script

```
Create a database migration script from {OLD_SCHEMA} to {NEW_SCHEMA}:
1. Map old tables to new tables
2. Handle column type changes
3. Preserve existing data
4. Add rollback capability
5. Include data validation
6. Add progress logging
7. Estimate execution time

Use Prisma migrate format.
```

## Template 10: Generate Progress Dashboard

```
Create a migration progress dashboard:
1. Scan all migration directories
2. Count files:
   - Total to migrate
   - Completed
   - In progress
   - Blocked
3. Calculate percentage complete
4. List critical path items
5. Show estimated completion date
6. Highlight risks and blockers

Output as markdown with visual indicators.
```
```

---

## ✅ Checklist: พร้อมเริ่ม Migration หรือยัง?

### Preparation Checklist

- [ ] **Backup existing system**
  - Database backup
  - Code repository backup
  - Configuration backup

- [ ] **Setup development environment**
  - Install Bun.js runtime
  - Setup Node.js (for tooling)
  - Install VS Code extensions
  - Configure TypeScript

- [ ] **Access to tools**
  - Claude Code installed and configured
  - Claude Cowork access (Team/Enterprise plan)
  - Git repository access
  - CI/CD platform access

- [ ] **Team alignment**
  - Migration plan reviewed and approved
  - Team trained on new stack
  - Communication channels setup
  - Escalation path defined

- [ ] **Documentation ready**
  - Architecture document created ✓
  - API contracts defined
  - Component library planned
  - Testing strategy documented

---

## 🎓 Learning Resources

### สิ่งที่ควรศึกษาก่อนเริ่ม Migration

1. **Bun.js Basics**
   - Runtime fundamentals
   - Package management
   - TypeScript support

2. **Elysia.js Framework**
   - Routing and middleware
   - TypeBox validation
   - Authentication
   - WebSocket

3. **React 18+**
   - Hooks and state management
   - React Query
   - React Router
   - Form handling

4. **Prisma ORM**
   - Schema definition
   - Migrations
   - Query API

5. **Testing**
   - Vitest (unit tests)
   - React Testing Library
   - Playwright (E2E)

---

## 📞 Support & Escalation

### ติดต่อเมื่อมีปัญหา

1. **Technical Issues**
   - Claude Code: Use `claude-code --help` or GitHub issues
   - Claude Cowork: Claude Desktop app support
   - Stack Overflow: Tag with `elysia`, `bun`, `react`

2. **Migration Blockers**
   - Document the issue clearly
   - Create minimal reproduction
   - Escalate to team lead
   - Consider alternative approaches

3. **Business Decisions**
   - Scope changes
   - Timeline adjustments
   - Resource allocation
   - Stakeholder communication

---

**หมายเหตุ:** คู่มือนี้เป็นจุดเริ่มต้น สามารถปรับแต่งตามความต้องการเฉพาะของโปรเจคได้

**Happy Migrating! 🚀**
