#!/usr/bin/env python3
"""
Setup new React + Elysia.js project structure
"""

import argparse
import json
import os
import subprocess
from pathlib import Path


def create_project_structure(project_name: str, output_dir: str = "."):
    """Create the new project directory structure"""
    
    base_path = Path(output_dir) / project_name
    
    # Create directories
    dirs = [
        "api/src/routes",
        "api/src/services",
        "api/src/schemas",
        "api/src/middleware",
        "api/prisma",
        "api/tests",
        "web/src/pages",
        "web/src/components",
        "web/src/services",
        "web/src/hooks",
        "web/src/types",
        "web/src/utils",
        "web/tests",
        "shared/types",
    ]
    
    for dir_path in dirs:
        (base_path / dir_path).mkdir(parents=True, exist_ok=True)
    
    print(f"✓ Created project structure at {base_path}")
    return base_path


def init_elysia_project(base_path: Path):
    """Initialize Elysia.js backend project"""
    
    api_path = base_path / "api"
    
    # Create package.json for API
    package_json = {
        "name": f"{base_path.name}-api",
        "version": "1.0.0",
        "type": "module",
        "scripts": {
            "dev": "bun run --watch src/index.ts",
            "start": "bun run src/index.ts",
            "test": "bun test",
            "prisma:generate": "prisma generate",
            "prisma:migrate": "prisma migrate dev",
            "prisma:studio": "prisma studio"
        },
        "dependencies": {
            "elysia": "latest",
            "@elysiajs/cors": "latest",
            "@elysiajs/jwt": "latest",
            "@elysiajs/swagger": "latest",
            "@prisma/client": "latest"
        },
        "devDependencies": {
            "prisma": "latest",
            "typescript": "latest",
            "@types/bun": "latest"
        }
    }
    
    with open(api_path / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)
    
    # Create main index.ts
    index_ts = """import { Elysia } from 'elysia'
import { cors } from '@elysiajs/cors'
import { swagger } from '@elysiajs/swagger'

const app = new Elysia()
  .use(cors())
  .use(swagger({
    documentation: {
      info: {
        title: 'API Documentation',
        version: '1.0.0'
      }
    }
  }))
  .get('/', () => 'Hello, World!')
  .listen(3000)

console.log(`🦊 API running at http://localhost:${app.server?.port}`)
console.log(`📚 Swagger docs at http://localhost:${app.server?.port}/swagger`)
"""
    
    with open(api_path / "src" / "index.ts", "w") as f:
        f.write(index_ts)
    
    # Create tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ESNext",
            "module": "ESNext",
            "moduleResolution": "bundler",
            "lib": ["ESNext"],
            "types": ["bun-types"],
            "jsx": "react-jsx",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "resolveJsonModule": True,
            "allowSyntheticDefaultImports": True,
            "outDir": "./dist",
            "rootDir": "./src",
            "baseUrl": ".",
            "paths": {
                "@/*": ["./src/*"]
            }
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
    
    with open(api_path / "tsconfig.json", "w") as f:
        json.dump(tsconfig, f, indent=2)
    
    # Create initial Prisma schema
    prisma_schema = """// This is your Prisma schema file,
// learn more about it in the docs: https://pris.ly/d/prisma-schema

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// Add your models here
// model User {
//   id        Int      @id @default(autoincrement())
//   email     String   @unique
//   name      String?
//   createdAt DateTime @default(now())
//   updatedAt DateTime @updatedAt
// }
"""
    
    with open(api_path / "prisma" / "schema.prisma", "w") as f:
        f.write(prisma_schema)
    
    # Create .env file
    env_file = """DATABASE_URL="postgresql://user:password@localhost:5432/mydb?schema=public"
JWT_SECRET="your-secret-key-here"
"""
    
    with open(api_path / ".env", "w") as f:
        f.write(env_file)
    
    print(f"✓ Initialized Elysia.js API project")


def init_react_project(base_path: Path):
    """Initialize React + Vite frontend project"""
    
    web_path = base_path / "web"
    
    # Create package.json for Web
    package_json = {
        "name": f"{base_path.name}-web",
        "version": "1.0.0",
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "tsc && vite build",
            "preview": "vite preview",
            "test": "vitest",
            "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
        },
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.20.0",
            "@tanstack/react-query": "^5.8.0",
            "axios": "^1.6.0",
            "react-hook-form": "^7.48.0",
            "zod": "^3.22.0",
            "zustand": "^4.4.0"
        },
        "devDependencies": {
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0",
            "@vitejs/plugin-react": "^4.2.0",
            "typescript": "^5.3.0",
            "vite": "^5.0.0",
            "vitest": "^1.0.0",
            "@testing-library/react": "^14.1.0",
            "@testing-library/jest-dom": "^6.1.0",
            "eslint": "^8.55.0",
            "eslint-plugin-react-hooks": "^4.6.0",
            "eslint-plugin-react-refresh": "^0.4.0",
            "tailwindcss": "^3.3.0",
            "postcss": "^8.4.0",
            "autoprefixer": "^10.4.0"
        }
    }
    
    with open(web_path / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)
    
    # Create vite.config.ts
    vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
    },
  },
})
"""
    
    with open(web_path / "vite.config.ts", "w") as f:
        f.write(vite_config)
    
    # Create main.tsx
    main_tsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'

const queryClient = new QueryClient()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
)
"""
    
    with open(web_path / "src" / "main.tsx", "w") as f:
        f.write(main_tsx)
    
    # Create App.tsx
    app_tsx = """import { Routes, Route } from 'react-router-dom'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Routes>
        <Route path="/" element={<div>Home Page</div>} />
        {/* Add your routes here */}
      </Routes>
    </div>
  )
}

export default App
"""
    
    with open(web_path / "src" / "App.tsx", "w") as f:
        f.write(app_tsx)
    
    # Create index.css (Tailwind)
    index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
"""
    
    with open(web_path / "src" / "index.css", "w") as f:
        f.write(index_css)
    
    # Create index.html
    index_html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>React App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""
    
    with open(web_path / "index.html", "w") as f:
        f.write(index_html)
    
    # Create tailwind.config.js
    tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
    
    with open(web_path / "tailwind.config.js", "w") as f:
        f.write(tailwind_config)
    
    # Create postcss.config.js
    postcss_config = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
    
    with open(web_path / "postcss.config.js", "w") as f:
        f.write(postcss_config)
    
    print(f"✓ Initialized React + Vite web project")


def create_shared_types(base_path: Path):
    """Create shared TypeScript types"""
    
    shared_path = base_path / "shared" / "types"
    
    # Create api.ts for shared API types
    api_types = """// Shared API types between frontend and backend

export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
}

export interface ApiError {
  message: string
  statusCode: number
  errors?: Record<string, string[]>
}
"""
    
    with open(shared_path / "api.ts", "w") as f:
        f.write(api_types)
    
    print(f"✓ Created shared TypeScript types")


def create_readme(base_path: Path, project_name: str):
    """Create main README.md"""
    
    readme = f"""# {project_name}

Migrated from C# ASP.NET Core Razor Pages to React + Bun.js + Elysia.js

## Project Structure

```
{project_name}/
├── api/          # Elysia.js backend
├── web/          # React frontend
└── shared/       # Shared types
```

## Getting Started

### Prerequisites

- Bun.js runtime: https://bun.sh
- Node.js 18+ (for tooling)
- PostgreSQL database

### Installation

1. Install API dependencies:
```bash
cd api
bun install
```

2. Install Web dependencies:
```bash
cd web
bun install
```

3. Setup database:
```bash
cd api
cp .env.example .env
# Edit .env with your database credentials
bunx prisma migrate dev
```

### Development

1. Start API server:
```bash
cd api
bun run dev
```

2. Start React dev server:
```bash
cd web
bun run dev
```

3. Open browser:
- Frontend: http://localhost:5173
- API: http://localhost:3000
- Swagger docs: http://localhost:3000/swagger

### Testing

```bash
# API tests
cd api
bun test

# Web tests
cd web
bun test
```

### Building for Production

```bash
# Build API
cd api
bun run build

# Build Web
cd web
bun run build
```

## Migration Notes

This project was migrated from C# ASP.NET Core Razor Pages using the csharp-to-react-migrator skill.

- Migration date: {datetime.now().strftime('%Y-%m-%d')}
- Original project: [Add link to original repo]
- Migration tool: OpenClaw Agent Skills
"""
    
    from datetime import datetime
    
    with open(base_path / "README.md", "w") as f:
        f.write(readme)
    
    print(f"✓ Created README.md")


def main():
    parser = argparse.ArgumentParser(
        description="Setup new React + Elysia.js project structure"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Project name"
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip installing dependencies"
    )
    
    args = parser.parse_args()
    
    print(f"🚀 Setting up project: {args.name}")
    print()
    
    # Create project structure
    base_path = create_project_structure(args.name, args.output)
    
    # Initialize projects
    init_elysia_project(base_path)
    init_react_project(base_path)
    create_shared_types(base_path)
    create_readme(base_path, args.name)
    
    print()
    print("✅ Project setup complete!")
    print()
    print("Next steps:")
    print(f"  1. cd {args.name}/api && bun install")
    print(f"  2. cd {args.name}/web && bun install")
    print(f"  3. Update api/.env with your database credentials")
    print(f"  4. cd api && bunx prisma migrate dev")
    print(f"  5. Start developing!")
    print()
    print(f"Project created at: {base_path.absolute()}")


if __name__ == "__main__":
    main()
