# C# to React + Elysia.js Migrator Skill

**Skill Name:** `csharp-to-react-migrator`

**Description:** Migrates C# ASP.NET Core Razor Pages projects to React + Bun.js + Elysia.js stack.

---

## 🎯 What This Skill Does

Automates the migration of:

- ✅ **C# Models** → Prisma Schemas
- ✅ **C# Handlers** → Elysia.js Routes
- ✅ **Razor Pages** → React Components
- ✅ **Entity Framework** → Prisma ORM
- ✅ **Server-side Logic** → Client-side + API

---

## 🚀 Quick Start

### 1. Setup New Project

```bash
python scripts/setup-project.py --name myproject
```

This creates:
```
myproject/
├── api/          (Elysia.js backend)
├── web/          (React frontend)
└── shared/       (Shared types)
```

### 2. Migrate Models

```bash
python scripts/convert-model.py Models/User.cs --output api/prisma/schema.prisma
```

### 3. Migrate Routes

```bash
python scripts/convert-handler.py Pages/Users/Index.cshtml.cs --output api/src/routes/
```

### 4. Migrate Pages

```bash
python scripts/convert-razor.py Pages/Users/Index.cshtml --output web/src/pages/
```

---

## 📚 Skill Structure

```
csharp-to-react-migrator/
├── SKILL.md                    # Main instructions (this file)
├── scripts/                    # Python automation scripts
│   ├── setup-project.py       # Create new project structure
│   ├── convert-model.py       # C# → Prisma
│   ├── convert-handler.py     # C# → Elysia
│   └── convert-razor.py       # Razor → React
├── references/                 # Documentation
│   ├── type-mapping.md        # C# to Prisma type mapping
│   ├── error-codes.md         # Common errors
│   └── patterns.md            # Migration patterns
└── assets/                     # Templates
    ├── elysia-route.template.ts
    ├── react-list-component.template.tsx
    └── prisma-schema.template.prisma
```

---

## 📖 Documentation

### For Agents

Agents should read `SKILL.md` for step-by-step migration instructions.

### For Humans

- **Type Mapping**: See `references/type-mapping.md`
- **Templates**: See `assets/` directory
- **Examples**: See main project `docs/migration-examples.md`

---

## 🔧 Scripts Reference

### setup-project.py

Creates new project structure with all necessary files.

```bash
python scripts/setup-project.py --name <project-name> [options]

Options:
  --output DIR         Output directory (default: current)
  --skip-install       Skip installing dependencies
```

### convert-model.py

Converts C# model classes to Prisma schema.

```bash
python scripts/convert-model.py <input.cs> [options]

Options:
  --output FILE        Output schema file
  --append             Append to existing schema
  --verbose            Show detailed output
```

### convert-handler.py

Converts C# Razor Page handlers to Elysia.js routes.

```bash
python scripts/convert-handler.py <input.cs> [options]

Options:
  --output DIR         Output directory for routes
  --verbose            Show detailed output
```

### convert-razor.py

Converts Razor Pages to React components.

```bash
python scripts/convert-razor.py <input.cshtml> [options]

Options:
  --output DIR         Output directory for components
  --verbose            Show detailed output
```

---

## ✅ Migration Checklist

After using this skill, verify:

- [ ] All models migrated to Prisma
- [ ] All handlers converted to Elysia routes
- [ ] All Razor pages converted to React
- [ ] API tests passing (>80% coverage)
- [ ] Component tests passing (>80% coverage)
- [ ] No TypeScript errors
- [ ] API documentation generated
- [ ] Authentication working
- [ ] Database migrations successful

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** Script fails with "No public class found"
**Solution:** Ensure the C# file contains a public class definition

**Issue:** Prisma type mapping incorrect
**Solution:** Check `references/type-mapping.md` for manual mapping

**Issue:** Complex LINQ queries not converted
**Solution:** Manual translation required (see `references/linq-to-prisma.md`)

### Error Recovery

1. Check error message in console
2. See `references/error-codes.md`
3. Fix the C# source file manually
4. Re-run script with `--verbose` flag
5. Use manual migration checklist in `assets/`

---

## 📝 Examples

### Example 1: Simple Model

**Input (C#):**
```csharp
public class User
{
    public int Id { get; set; }
    public string Username { get; set; }
    public string Email { get; set; }
}
```

**Output (Prisma):**
```prisma
model User {
  id       Int    @id @default(autoincrement())
  username String @db.VarChar(255)
  email    String @db.VarChar(255)
  
  @@map("users")
}
```

### Example 2: Handler to Route

**Input (C#):**
```csharp
public async Task OnGetAsync()
{
    Users = await _context.Users.ToListAsync();
}
```

**Output (Elysia):**
```typescript
.get('/', async () => {
  return await prisma.user.findMany()
})
```

### Example 3: Razor to React

**Input (Razor):**
```cshtml
@foreach (var user in Model.Users)
{
    <p>@user.Username</p>
}
```

**Output (React):**
```tsx
{users.map(user => (
  <p key={user.id}>{user.username}</p>
))}
```

---

## 🔗 Related Resources

- **Architecture Document**: `/docs/migration-architecture-csharp-to-react-bun-elysia.md`
- **Examples**: `/docs/migration-examples.md`
- **Claude Code Guide**: `/docs/claude-code-cowork-guide.md`

---

## 📊 Skill Metadata

- **Version**: 1.0.0
- **Author**: OpenClaw Agent Skills
- **Created**: 2026-02-27
- **Last Updated**: 2026-02-27
- **License**: MIT

---

## 🤝 Contributing

To improve this skill:

1. Add new scripts for additional conversion patterns
2. Update type mappings in references
3. Add more templates in assets
4. Improve error handling
5. Add more test cases

---

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section
2. Review the references directory
3. Consult the main migration documentation
4. Open an issue in the project repository

---

**Note:** This skill is designed for C# ASP.NET Core Razor Pages projects. It may not work correctly for other project types (MVC, Web API, Blazor, etc.).
