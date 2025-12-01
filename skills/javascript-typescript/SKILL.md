---
name: workbench:javascript-typescript
description: Expert JavaScript and TypeScript development covering modern ES6+ patterns, advanced types, async programming, Node.js backends, and testing. Use for writing production-grade JS/TS code.
when_to_use: When writing JavaScript or TypeScript. When building Node.js backends. When working with async patterns. When designing type systems. When writing tests with Jest/Vitest.
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# JavaScript & TypeScript Expert

**Announce at start:** "I'm using the javascript-typescript skill for JS/TS development."

## Overview

Production-grade JavaScript and TypeScript development with modern patterns, type safety, and best practices.

**Core principle:** Write type-safe, maintainable code that leverages modern language features.

## Quick Reference

| Task | Approach |
|------|----------|
| New project | TypeScript strict mode, ESM modules, Vitest |
| Async code | async/await, proper error handling |
| Types | Leverage inference, generics for reusability |
| Testing | AAA pattern, mock external deps only |

## Modern JavaScript (ES6+)

### Destructuring & Spread

```javascript
// Object destructuring with defaults
const { name, age = 0, ...rest } = user;

// Array destructuring
const [first, second, ...remaining] = items;

// Spread for immutable updates
const updated = { ...user, name: 'New Name' };
const combined = [...arr1, ...arr2];
```

### Arrow Functions

```javascript
// Lexical this binding
const handler = {
  items: [],
  process() {
    // Arrow preserves 'this'
    this.items.forEach(item => this.handle(item));
  }
};

// Implicit return
const double = x => x * 2;
const getUser = id => ({ id, name: 'User' });
```

### Template Literals

```javascript
// Multiline and interpolation
const html = `
  <div class="${className}">
    ${items.map(i => `<span>${i}</span>`).join('')}
  </div>
`;

// Tagged templates
function sql(strings, ...values) {
  return { text: strings.join('$'), values };
}
const query = sql`SELECT * FROM users WHERE id = ${userId}`;
```

## Async Patterns

### async/await

```javascript
// Prefer async/await over .then() chains
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error;
  }
}
```

### Parallel vs Sequential

```javascript
// Parallel - when operations are independent
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
]);

// Sequential - when order matters
const user = await fetchUser(id);
const posts = await fetchUserPosts(user.id);

// Promise.allSettled - when you need all results
const results = await Promise.allSettled([
  fetchA(),
  fetchB(),
  fetchC()
]);
const succeeded = results.filter(r => r.status === 'fulfilled');
```

### Retry Logic

```javascript
async function withRetry(fn, maxAttempts = 3, delay = 1000) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      await new Promise(r => setTimeout(r, delay * attempt));
    }
  }
}
```

### Timeout Wrapper

```javascript
function withTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Timeout')), ms)
  );
  return Promise.race([promise, timeout]);
}
```

## TypeScript Types

### Generics

```typescript
// Basic generic function
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

// Constrained generics
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Generic class
class Repository<T extends { id: string }> {
  private items: Map<string, T> = new Map();

  save(item: T): void {
    this.items.set(item.id, item);
  }

  findById(id: string): T | undefined {
    return this.items.get(id);
  }
}
```

### Utility Types

```typescript
// Built-in utilities
type UserPartial = Partial<User>;           // All optional
type UserRequired = Required<User>;         // All required
type UserReadonly = Readonly<User>;         // All readonly
type UserName = Pick<User, 'name' | 'email'>;
type UserWithoutId = Omit<User, 'id'>;

// Record for dictionaries
type UserMap = Record<string, User>;

// Extract/Exclude for unions
type StringOrNumber = Extract<string | number | boolean, string | number>;
```

### Conditional Types

```typescript
// Basic conditional
type IsString<T> = T extends string ? true : false;

// Infer keyword
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type ArrayElement<T> = T extends (infer E)[] ? E : never;

// Distributive conditional
type NonNullable<T> = T extends null | undefined ? never : T;
```

### Mapped Types

```typescript
// Make all properties optional
type Optional<T> = { [K in keyof T]?: T[K] };

// Add prefix to keys
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
};

// Filter by value type
type StringKeys<T> = {
  [K in keyof T]: T[K] extends string ? K : never
}[keyof T];
```

### Discriminated Unions

```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function handle<T>(result: Result<T>) {
  if (result.success) {
    console.log(result.data);  // T
  } else {
    console.error(result.error);  // Error
  }
}

// State machine
type State =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: User }
  | { status: 'error'; error: Error };
```

## Node.js Backend

### Express Setup

```typescript
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';

const app = express();

// Security middleware
app.use(helmet());
app.use(cors({ origin: process.env.ALLOWED_ORIGINS?.split(',') }));
app.use(compression());
app.use(express.json({ limit: '10kb' }));

// Request logging
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    console.log(`${req.method} ${req.path} ${res.statusCode} ${Date.now() - start}ms`);
  });
  next();
});
```

### Layered Architecture

```
src/
├── controllers/    # HTTP request/response
├── services/       # Business logic
├── repositories/   # Data access
├── models/         # Data structures
├── middleware/     # Request processing
└── utils/          # Helpers
```

```typescript
// Controller
export class UserController {
  constructor(private userService: UserService) {}

  async getUser(req: Request, res: Response) {
    const user = await this.userService.findById(req.params.id);
    if (!user) return res.status(404).json({ error: 'Not found' });
    res.json(user);
  }
}

// Service
export class UserService {
  constructor(private userRepo: UserRepository) {}

  async findById(id: string): Promise<User | null> {
    return this.userRepo.findById(id);
  }
}
```

### Error Handling

```typescript
// Custom error class
class AppError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public isOperational = true
  ) {
    super(message);
    Error.captureStackTrace(this, this.constructor);
  }
}

// Global error handler
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      status: 'error',
      message: err.message
    });
  }

  console.error('Unexpected error:', err);
  res.status(500).json({
    status: 'error',
    message: 'Internal server error'
  });
});
```

### Validation with Zod

```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().positive().optional()
});

type CreateUserInput = z.infer<typeof CreateUserSchema>;

function validateBody<T>(schema: z.ZodSchema<T>) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ errors: result.error.flatten() });
    }
    req.body = result.data;
    next();
  };
}

app.post('/users', validateBody(CreateUserSchema), createUser);
```

## Testing

### Test Structure (AAA)

```typescript
describe('UserService', () => {
  let service: UserService;
  let mockRepo: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepo = { findById: jest.fn() } as any;
    service = new UserService(mockRepo);
  });

  describe('findById', () => {
    it('returns user when found', async () => {
      // Arrange
      const expectedUser = { id: '1', name: 'Test' };
      mockRepo.findById.mockResolvedValue(expectedUser);

      // Act
      const result = await service.findById('1');

      // Assert
      expect(result).toEqual(expectedUser);
      expect(mockRepo.findById).toHaveBeenCalledWith('1');
    });

    it('returns null when not found', async () => {
      mockRepo.findById.mockResolvedValue(null);

      const result = await service.findById('999');

      expect(result).toBeNull();
    });
  });
});
```

### Async Testing

```typescript
// Testing promises
it('handles async errors', async () => {
  await expect(fetchUser('invalid')).rejects.toThrow('Not found');
});

// Testing with fake timers
it('retries on failure', async () => {
  vi.useFakeTimers();
  const fn = vi.fn()
    .mockRejectedValueOnce(new Error('Fail'))
    .mockResolvedValueOnce('success');

  const promise = withRetry(fn, 2, 1000);
  await vi.advanceTimersByTimeAsync(1000);

  await expect(promise).resolves.toBe('success');
  expect(fn).toHaveBeenCalledTimes(2);
});
```

### React Component Testing

```typescript
import { render, screen, fireEvent } from '@testing-library/react';

it('calls onSubmit with form data', async () => {
  const onSubmit = vi.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  await userEvent.type(screen.getByLabelText('Email'), 'test@example.com');
  await userEvent.type(screen.getByLabelText('Password'), 'password123');
  await userEvent.click(screen.getByRole('button', { name: 'Login' }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
    password: 'password123'
  });
});
```

## Project Setup

### tsconfig.json (Strict)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true,
    "incremental": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### Package Scripts

```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "vitest",
    "test:coverage": "vitest run --coverage",
    "lint": "eslint src --ext .ts,.tsx",
    "typecheck": "tsc --noEmit"
  }
}
```

## Best Practices

### Do

- Use `const` by default, `let` when reassignment needed
- Prefer `async/await` over promise chains
- Leverage TypeScript inference (don't over-annotate)
- Use strict TypeScript settings
- Write small, focused functions
- Handle errors explicitly
- Use destructuring for cleaner code
- Prefer immutable operations

### Avoid

- `any` type (use `unknown` if type is truly unknown)
- Nested callbacks (use async/await)
- Mutating function arguments
- `==` (use `===`)
- `var` (use `const`/`let`)
- Implicit type coercion
- Blocking the event loop
- Catching errors without handling them

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| `this` undefined in callback | Arrow function or `.bind()` |
| Unhandled promise rejection | Always `catch` or use try/catch |
| Type assertion abuse | Proper type guards |
| Floating promises | `await` or explicit `.catch()` |
| Optional chaining overuse | Check business logic validity |
