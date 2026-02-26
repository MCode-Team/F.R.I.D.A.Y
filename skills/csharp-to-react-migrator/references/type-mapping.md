# C# to Prisma Type Mapping

## Basic Types

| C# Type | Prisma Type | Notes |
|---------|-------------|-------|
| `int` | `Int` | 32-bit integer |
| `long` | `BigInt` | 64-bit integer |
| `short` | `Int` | 16-bit integer |
| `byte` | `Int` | 8-bit integer |
| `float` | `Float` | Single-precision |
| `double` | `Float` | Double-precision |
| `decimal` | `Decimal` | Fixed-precision |
| `bool` | `Boolean` | true/false |
| `string` | `String` | UTF-8 string |
| `char` | `String` | Single character |
| `DateTime` | `DateTime` | Date and time |
| `DateTimeOffset` | `DateTime` | With timezone |
| `Guid` | `String` | UUID as string |
| `byte[]` | `Bytes` | Binary data |

## Nullable Types

C# nullable types (`Type?`) map to Prisma optional fields:

**C#:**
```csharp
public string? MiddleName { get; set; }
```

**Prisma:**
```prisma
middleName String?
```

## Collections

C# collections map to Prisma relations:

**C#:**
```csharp
public class User
{
    public int Id { get; set; }
    public List<Order> Orders { get; set; }
}

public class Order
{
    public int Id { get; set; }
    public int UserId { get; set; }
    public User User { get; set; }
}
```

**Prisma:**
```prisma
model User {
  id     Int      @id @default(autoincrement())
  orders Order[]
}

model Order {
  id     Int  @id @default(autoincrement())
  userId Int
  user   User @relation(fields: [userId], references: [id])
}
```

## DataAnnotations to Prisma Attributes

### [Required]

**C#:**
```csharp
[Required]
public string Username { get; set; }
```

**Prisma:**
```prisma
username String @db.VarChar(255)
```

Note: Prisma doesn't have a "required" attribute, non-nullable types are required by default.

### [StringLength]

**C#:**
```csharp
[StringLength(50)]
public string Username { get; set; }
```

**Prisma:**
```prisma
username String @db.VarChar(50)
```

### [EmailAddress]

**C#:**
```csharp
[EmailAddress]
public string Email { get; set; }
```

**Prisma:**
```prisma
email String @db.VarChar(255)
```

Note: Prisma doesn't validate email format, this is application-level validation.

### [Key]

**C#:**
```csharp
[Key]
public int Id { get; set; }
```

**Prisma:**
```prisma
id Int @id @default(autoincrement())
```

### [Range]

**C#:**
```csharp
[Range(0, 100)]
public int Age { get; set; }
```

**Prisma:**
```prisma
age Int
```

Note: Range validation must be done at application level with TypeBox.

### [MinLength] / [MaxLength]

**C#:**
```csharp
[MaxLength(500)]
public string Description { get; set; }
```

**Prisma:**
```prisma
description String? @db.VarChar(500)
```

## Common Patterns

### CreatedAt / UpdatedAt

**C#:**
```csharp
public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
public DateTime? UpdatedAt { get; set; }
```

**Prisma:**
```prisma
createdAt DateTime @default(now())
updatedAt DateTime @updatedAt
```

### Soft Delete

**C#:**
```csharp
public bool IsDeleted { get; set; } = false;
public DateTime? DeletedAt { get; set; }
```

**Prisma:**
```prisma
isDeleted  Boolean   @default(false)
deletedAt  DateTime?
```

### Status/Enum

**C#:**
```csharp
public enum UserStatus
{
    Active,
    Inactive,
    Suspended
}

public UserStatus Status { get; set; }
```

**Prisma:**
```prisma
enum UserStatus {
  Active
  Inactive
  Suspended
}

model User {
  status UserStatus @default(Active)
}
```

### Money/Price

**C#:**
```csharp
public decimal Price { get; set; }
```

**Prisma:**
```prisma
price Decimal @db.Decimal(10, 2)
```

### JSON Column

**C#:**
```csharp
public string Metadata { get; set; } // JSON serialized
```

**Prisma:**
```prisma
metadata Json
```

## Relationships

### One-to-Many

**C#:**
```csharp
public class Author
{
    public int Id { get; set; }
    public ICollection<Book> Books { get; set; }
}

public class Book
{
    public int Id { get; set; }
    public int AuthorId { get; set; }
    public Author Author { get; set; }
}
```

**Prisma:**
```prisma
model Author {
  id    Int    @id @default(autoincrement())
  books Book[]
}

model Book {
  id       Int    @id @default(autoincrement())
  authorId Int
  author   Author @relation(fields: [authorId], references: [id])
}
```

### Many-to-Many

**C#:**
```csharp
public class Student
{
    public int Id { get; set; }
    public ICollection<Course> Courses { get; set; }
}

public class Course
{
    public int Id { get; set; }
    public ICollection<Student> Students { get; set; }
}
```

**Prisma:**
```prisma
model Student {
  id      Int       @id @default(autoincrement())
  courses Course[]  @relation("StudentCourses")
}

model Course {
  id       Int      @id @default(autoincrement())
  students Student[] @relation("StudentCourses")
}
```

Note: Prisma creates an implicit join table for many-to-many relationships.

### Self-Referencing

**C#:**
```csharp
public class Category
{
    public int Id { get; set; }
    public int? ParentId { get; set; }
    public Category Parent { get; set; }
    public ICollection<Category> Children { get; set; }
}
```

**Prisma:**
```prisma
model Category {
  id       Int         @id @default(autoincrement())
  parentId Int?
  parent   Category?   @relation("CategoryTree", fields: [parentId], references: [id])
  children Category[]  @relation("CategoryTree")
}
```

## Indexes

### Single Field Index

**C#:**
```csharp
// Usually done with Fluent API or conventions
public string Email { get; set; }
```

**Prisma:**
```prisma
model User {
  email String @unique
  
  @@index([email])
}
```

### Composite Index

**Prisma:**
```prisma
model User {
  firstName String
  lastName  String
  
  @@index([firstName, lastName])
}
```

### Unique Constraint

**C#:**
```csharp
[Index(nameof(Email), IsUnique = true)]
public class User
{
    public string Email { get; set; }
}
```

**Prisma:**
```prisma
model User {
  email String @unique
}
```

## Notes

1. **Validation**: Prisma schema validation is minimal. Most DataAnnotations should be implemented with TypeBox in the API layer.

2. **Default Values**: Prisma supports `@default()` for automatic values. Map C# default values to Prisma defaults.

3. **Database-Specific Types**: Use `@db.` prefix for database-specific types (e.g., `@db.VarChar(255)`, `@db.Text`).

4. **Naming Convention**: 
   - C#: PascalCase
   - Prisma: camelCase for fields
   - Database: snake_case (use `@@map()` to customize table names)

5. **Migrations**: After generating schema, run `prisma migrate dev` to create database tables.
