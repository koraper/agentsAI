---
name: nodejs-backend-patterns
description: 빌드 프로덕션 준비 완료 Node.js backend 서비스 와 함께 Express/Fastify, implementing 미들웨어 패턴, 오류 처리, 인증, 데이터베이스 통합, 및 API 설계 최선의 관행. Use 때 생성하는 Node.js 서버, REST APIs, GraphQL backends, 또는 microservices 아키텍처.
---

# Node.js Backend 패턴

포괄적인 guidance 위한 구축 scalable, maintainable, 및 프로덕션 준비 완료 Node.js backend 애플리케이션 와 함께 현대적인 프레임워크, architectural 패턴, 및 최선의 관행.

## 때 에 Use This Skill

- 구축 REST APIs 또는 GraphQL 서버
- 생성하는 microservices 와 함께 Node.js
- Implementing 인증 및 인가
- Designing scalable backend 아키텍처
- 설정하는 미들웨어 및 오류 처리
- Integrating databases (SQL 및 NoSQL)
- 구축 real-시간 애플리케이션 와 함께 WebSockets
- Implementing background 작업 처리

## 핵심 프레임워크

### Express.js - Minimalist 프레임워크

**기본 설정:**
```typescript
import express, { Request, Response, NextFunction } from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';

const app = express();

// Security middleware
app.use(helmet());
app.use(cors({ origin: process.env.ALLOWED_ORIGINS?.split(',') }));
app.use(compression());

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Request logging
app.use((req: Request, res: Response, next: NextFunction) => {
  console.log(`${req.method} ${req.path}`);
  next();
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Fastify - High 성능 프레임워크

**기본 설정:**
```typescript
import Fastify from 'fastify';
import helmet from '@fastify/helmet';
import cors from '@fastify/cors';
import compress from '@fastify/compress';

const fastify = Fastify({
  logger: {
    level: process.env.LOG_LEVEL || 'info',
    transport: {
      target: 'pino-pretty',
      options: { colorize: true }
    }
  }
});

// Plugins
await fastify.register(helmet);
await fastify.register(cors, { origin: true });
await fastify.register(compress);

// Type-safe routes with schema validation
fastify.post<{
  Body: { name: string; email: string };
  Reply: { id: string; name: string };
}>('/users', {
  schema: {
    body: {
      type: 'object',
      required: ['name', 'email'],
      properties: {
        name: { type: 'string', minLength: 1 },
        email: { type: 'string', format: 'email' }
      }
    }
  }
}, async (request, reply) => {
  const { name, email } = request.body;
  return { id: '123', name };
});

await fastify.listen({ port: 3000, host: '0.0.0.0' });
```

## Architectural 패턴

### 패턴 1: Layered 아키텍처

**구조:**
```
src/
├── controllers/     # Handle HTTP requests/responses
├── services/        # Business logic
├── repositories/    # Data access layer
├── models/          # Data models
├── middleware/      # Express/Fastify middleware
├── routes/          # Route definitions
├── utils/           # Helper functions
├── config/          # Configuration
└── types/           # TypeScript types
```

**컨트롤러 레이어:**
```typescript
// controllers/user.controller.ts
import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/user.service';
import { CreateUserDTO, UpdateUserDTO } from '../types/user.types';

export class UserController {
  constructor(private userService: UserService) {}

  async createUser(req: Request, res: Response, next: NextFunction) {
    try {
      const userData: CreateUserDTO = req.body;
      const user = await this.userService.createUser(userData);
      res.status(201).json(user);
    } catch (error) {
      next(error);
    }
  }

  async getUser(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      const user = await this.userService.getUserById(id);
      res.json(user);
    } catch (error) {
      next(error);
    }
  }

  async updateUser(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      const updates: UpdateUserDTO = req.body;
      const user = await this.userService.updateUser(id, updates);
      res.json(user);
    } catch (error) {
      next(error);
    }
  }

  async deleteUser(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      await this.userService.deleteUser(id);
      res.status(204).send();
    } catch (error) {
      next(error);
    }
  }
}
```

**서비스 레이어:**
```typescript
// services/user.service.ts
import { UserRepository } from '../repositories/user.repository';
import { CreateUserDTO, UpdateUserDTO, User } from '../types/user.types';
import { NotFoundError, ValidationError } from '../utils/errors';
import bcrypt from 'bcrypt';

export class UserService {
  constructor(private userRepository: UserRepository) {}

  async createUser(userData: CreateUserDTO): Promise<User> {
    // Validation
    const existingUser = await this.userRepository.findByEmail(userData.email);
    if (existingUser) {
      throw new ValidationError('Email already exists');
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(userData.password, 10);

    // Create user
    const user = await this.userRepository.create({
      ...userData,
      password: hashedPassword
    });

    // Remove password from response
    const { password, ...userWithoutPassword } = user;
    return userWithoutPassword as User;
  }

  async getUserById(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new NotFoundError('User not found');
    }
    const { password, ...userWithoutPassword } = user;
    return userWithoutPassword as User;
  }

  async updateUser(id: string, updates: UpdateUserDTO): Promise<User> {
    const user = await this.userRepository.update(id, updates);
    if (!user) {
      throw new NotFoundError('User not found');
    }
    const { password, ...userWithoutPassword } = user;
    return userWithoutPassword as User;
  }

  async deleteUser(id: string): Promise<void> {
    const deleted = await this.userRepository.delete(id);
    if (!deleted) {
      throw new NotFoundError('User not found');
    }
  }
}
```

**저장소 레이어:**
```typescript
// repositories/user.repository.ts
import { Pool } from 'pg';
import { CreateUserDTO, UpdateUserDTO, UserEntity } from '../types/user.types';

export class UserRepository {
  constructor(private db: Pool) {}

  async create(userData: CreateUserDTO & { password: string }): Promise<UserEntity> {
    const query = `
      INSERT INTO users (name, email, password)
      VALUES ($1, $2, $3)
      RETURNING id, name, email, password, created_at, updated_at
    `;
    const { rows } = await this.db.query(query, [
      userData.name,
      userData.email,
      userData.password
    ]);
    return rows[0];
  }

  async findById(id: string): Promise<UserEntity | null> {
    const query = 'SELECT * FROM users WHERE id = $1';
    const { rows } = await this.db.query(query, [id]);
    return rows[0] || null;
  }

  async findByEmail(email: string): Promise<UserEntity | null> {
    const query = 'SELECT * FROM users WHERE email = $1';
    const { rows } = await this.db.query(query, [email]);
    return rows[0] || null;
  }

  async update(id: string, updates: UpdateUserDTO): Promise<UserEntity | null> {
    const fields = Object.keys(updates);
    const values = Object.values(updates);

    const setClause = fields
      .map((field, idx) => `${field} = $${idx + 2}`)
      .join(', ');

    const query = `
      UPDATE users
      SET ${setClause}, updated_at = CURRENT_TIMESTAMP
      WHERE id = $1
      RETURNING *
    `;

    const { rows } = await this.db.query(query, [id, ...values]);
    return rows[0] || null;
  }

  async delete(id: string): Promise<boolean> {
    const query = 'DELETE FROM users WHERE id = $1';
    const { rowCount } = await this.db.query(query, [id]);
    return rowCount > 0;
  }
}
```

### 패턴 2: 종속성 인젝션

**DI 컨테이너:**
```typescript
// di-container.ts
import { Pool } from 'pg';
import { UserRepository } from './repositories/user.repository';
import { UserService } from './services/user.service';
import { UserController } from './controllers/user.controller';
import { AuthService } from './services/auth.service';

class Container {
  private instances = new Map<string, any>();

  register<T>(key: string, factory: () => T): void {
    this.instances.set(key, factory);
  }

  resolve<T>(key: string): T {
    const factory = this.instances.get(key);
    if (!factory) {
      throw new Error(`No factory registered for ${key}`);
    }
    return factory();
  }

  singleton<T>(key: string, factory: () => T): void {
    let instance: T;
    this.instances.set(key, () => {
      if (!instance) {
        instance = factory();
      }
      return instance;
    });
  }
}

export const container = new Container();

// Register dependencies
container.singleton('db', () => new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
}));

container.singleton('userRepository', () =>
  new UserRepository(container.resolve('db'))
);

container.singleton('userService', () =>
  new UserService(container.resolve('userRepository'))
);

container.register('userController', () =>
  new UserController(container.resolve('userService'))
);

container.singleton('authService', () =>
  new AuthService(container.resolve('userRepository'))
);
```

## 미들웨어 패턴

### 인증 미들웨어

```typescript
// middleware/auth.middleware.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { UnauthorizedError } from '../utils/errors';

interface JWTPayload {
  userId: string;
  email: string;
}

declare global {
  namespace Express {
    interface Request {
      user?: JWTPayload;
    }
  }
}

export const authenticate = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');

    if (!token) {
      throw new UnauthorizedError('No token provided');
    }

    const payload = jwt.verify(
      token,
      process.env.JWT_SECRET!
    ) as JWTPayload;

    req.user = payload;
    next();
  } catch (error) {
    next(new UnauthorizedError('Invalid token'));
  }
};

export const authorize = (...roles: string[]) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return next(new UnauthorizedError('Not authenticated'));
    }

    // Check if user has required role
    const hasRole = roles.some(role =>
      req.user?.roles?.includes(role)
    );

    if (!hasRole) {
      return next(new UnauthorizedError('Insufficient permissions'));
    }

    next();
  };
};
```

### 검증 미들웨어

```typescript
// middleware/validation.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { AnyZodObject, ZodError } from 'zod';
import { ValidationError } from '../utils/errors';

export const validate = (schema: AnyZodObject) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      await schema.parseAsync({
        body: req.body,
        query: req.query,
        params: req.params
      });
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        const errors = error.errors.map(err => ({
          field: err.path.join('.'),
          message: err.message
        }));
        next(new ValidationError('Validation failed', errors));
      } else {
        next(error);
      }
    }
  };
};

// Usage with Zod
import { z } from 'zod';

const createUserSchema = z.object({
  body: z.object({
    name: z.string().min(1),
    email: z.string().email(),
    password: z.string().min(8)
  })
});

router.post('/users', validate(createUserSchema), userController.createUser);
```

### 속도 제한 미들웨어

```typescript
// middleware/rate-limit.middleware.ts
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import Redis from 'ioredis';

const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: parseInt(process.env.REDIS_PORT || '6379')
});

export const apiLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:',
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
});

export const authLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:auth:',
  }),
  windowMs: 15 * 60 * 1000,
  max: 5, // Stricter limit for auth endpoints
  skipSuccessfulRequests: true,
});
```

### 요청 로깅 미들웨어

```typescript
// middleware/logger.middleware.ts
import { Request, Response, NextFunction } from 'express';
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    target: 'pino-pretty',
    options: { colorize: true }
  }
});

export const requestLogger = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const start = Date.now();

  // Log response when finished
  res.on('finish', () => {
    const duration = Date.now() - start;
    logger.info({
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: `${duration}ms`,
      userAgent: req.headers['user-agent'],
      ip: req.ip
    });
  });

  next();
};

export { logger };
```

## 오류 처리

### 사용자 정의 오류 클래스

```typescript
// utils/errors.ts
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public isOperational: boolean = true
  ) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(message: string, public errors?: any[]) {
    super(message, 400);
  }
}

export class NotFoundError extends AppError {
  constructor(message: string = 'Resource not found') {
    super(message, 404);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message: string = 'Unauthorized') {
    super(message, 401);
  }
}

export class ForbiddenError extends AppError {
  constructor(message: string = 'Forbidden') {
    super(message, 403);
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super(message, 409);
  }
}
```

### 전역 오류 핸들러

```typescript
// middleware/error-handler.ts
import { Request, Response, NextFunction } from 'express';
import { AppError } from '../utils/errors';
import { logger } from './logger.middleware';

export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      status: 'error',
      message: err.message,
      ...(err instanceof ValidationError && { errors: err.errors })
    });
  }

  // Log unexpected errors
  logger.error({
    error: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method
  });

  // Don't leak error details in production
  const message = process.env.NODE_ENV === 'production'
    ? 'Internal server error'
    : err.message;

  res.status(500).json({
    status: 'error',
    message
  });
};

// Async error wrapper
export const asyncHandler = (
  fn: (req: Request, res: Response, next: NextFunction) => Promise<any>
) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};
```

## 데이터베이스 패턴

### PostgreSQL 와 함께 연결 풀

```typescript
// config/database.ts
import { Pool, PoolConfig } from 'pg';

const poolConfig: PoolConfig = {
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
};

export const pool = new Pool(poolConfig);

// Test connection
pool.on('connect', () => {
  console.log('Database connected');
});

pool.on('error', (err) => {
  console.error('Unexpected database error', err);
  process.exit(-1);
});

// Graceful shutdown
export const closeDatabase = async () => {
  await pool.end();
  console.log('Database connection closed');
};
```

### MongoDB 와 함께 Mongoose

```typescript
// config/mongoose.ts
import mongoose from 'mongoose';

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI!, {
      maxPoolSize: 10,
      serverSelectionTimeoutMS: 5000,
      socketTimeoutMS: 45000,
    });

    console.log('MongoDB connected');
  } catch (error) {
    console.error('MongoDB connection error:', error);
    process.exit(1);
  }
};

mongoose.connection.on('disconnected', () => {
  console.log('MongoDB disconnected');
});

mongoose.connection.on('error', (err) => {
  console.error('MongoDB error:', err);
});

export { connectDB };

// Model example
import { Schema, model, Document } from 'mongoose';

interface IUser extends Document {
  name: string;
  email: string;
  password: string;
  createdAt: Date;
  updatedAt: Date;
}

const userSchema = new Schema<IUser>({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
}, {
  timestamps: true
});

// Indexes
userSchema.index({ email: 1 });

export const User = model<IUser>('User', userSchema);
```

### 트랜잭션 패턴

```typescript
// services/order.service.ts
import { Pool } from 'pg';

export class OrderService {
  constructor(private db: Pool) {}

  async createOrder(userId: string, items: any[]) {
    const client = await this.db.connect();

    try {
      await client.query('BEGIN');

      // Create order
      const orderResult = await client.query(
        'INSERT INTO orders (user_id, total) VALUES ($1, $2) RETURNING id',
        [userId, calculateTotal(items)]
      );
      const orderId = orderResult.rows[0].id;

      // Create order items
      for (const item of items) {
        await client.query(
          'INSERT INTO order_items (order_id, product_id, quantity, price) VALUES ($1, $2, $3, $4)',
          [orderId, item.productId, item.quantity, item.price]
        );

        // Update inventory
        await client.query(
          'UPDATE products SET stock = stock - $1 WHERE id = $2',
          [item.quantity, item.productId]
        );
      }

      await client.query('COMMIT');
      return orderId;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }
}
```

## 인증 & 인가

### JWT 인증

```typescript
// services/auth.service.ts
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';
import { UserRepository } from '../repositories/user.repository';
import { UnauthorizedError } from '../utils/errors';

export class AuthService {
  constructor(private userRepository: UserRepository) {}

  async login(email: string, password: string) {
    const user = await this.userRepository.findByEmail(email);

    if (!user) {
      throw new UnauthorizedError('Invalid credentials');
    }

    const isValid = await bcrypt.compare(password, user.password);

    if (!isValid) {
      throw new UnauthorizedError('Invalid credentials');
    }

    const token = this.generateToken({
      userId: user.id,
      email: user.email
    });

    const refreshToken = this.generateRefreshToken({
      userId: user.id
    });

    return {
      token,
      refreshToken,
      user: {
        id: user.id,
        name: user.name,
        email: user.email
      }
    };
  }

  async refreshToken(refreshToken: string) {
    try {
      const payload = jwt.verify(
        refreshToken,
        process.env.REFRESH_TOKEN_SECRET!
      ) as { userId: string };

      const user = await this.userRepository.findById(payload.userId);

      if (!user) {
        throw new UnauthorizedError('User not found');
      }

      const token = this.generateToken({
        userId: user.id,
        email: user.email
      });

      return { token };
    } catch (error) {
      throw new UnauthorizedError('Invalid refresh token');
    }
  }

  private generateToken(payload: any): string {
    return jwt.sign(payload, process.env.JWT_SECRET!, {
      expiresIn: '15m'
    });
  }

  private generateRefreshToken(payload: any): string {
    return jwt.sign(payload, process.env.REFRESH_TOKEN_SECRET!, {
      expiresIn: '7d'
    });
  }
}
```

## 캐싱 Strategies

```typescript
// utils/cache.ts
import Redis from 'ioredis';

const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: parseInt(process.env.REDIS_PORT || '6379'),
  retryStrategy: (times) => {
    const delay = Math.min(times * 50, 2000);
    return delay;
  }
});

export class CacheService {
  async get<T>(key: string): Promise<T | null> {
    const data = await redis.get(key);
    return data ? JSON.parse(data) : null;
  }

  async set(key: string, value: any, ttl?: number): Promise<void> {
    const serialized = JSON.stringify(value);
    if (ttl) {
      await redis.setex(key, ttl, serialized);
    } else {
      await redis.set(key, serialized);
    }
  }

  async delete(key: string): Promise<void> {
    await redis.del(key);
  }

  async invalidatePattern(pattern: string): Promise<void> {
    const keys = await redis.keys(pattern);
    if (keys.length > 0) {
      await redis.del(...keys);
    }
  }
}

// Cache decorator
export function Cacheable(ttl: number = 300) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const cache = new CacheService();
      const cacheKey = `${propertyKey}:${JSON.stringify(args)}`;

      const cached = await cache.get(cacheKey);
      if (cached) {
        return cached;
      }

      const result = await originalMethod.apply(this, args);
      await cache.set(cacheKey, result, ttl);

      return result;
    };

    return descriptor;
  };
}
```

## API 응답 Format

```typescript
// utils/response.ts
import { Response } from 'express';

export class ApiResponse {
  static success<T>(res: Response, data: T, message?: string, statusCode = 200) {
    return res.status(statusCode).json({
      status: 'success',
      message,
      data
    });
  }

  static error(res: Response, message: string, statusCode = 500, errors?: any) {
    return res.status(statusCode).json({
      status: 'error',
      message,
      ...(errors && { errors })
    });
  }

  static paginated<T>(
    res: Response,
    data: T[],
    page: number,
    limit: number,
    total: number
  ) {
    return res.json({
      status: 'success',
      data,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    });
  }
}
```

## 최선의 관행

1. **Use TypeScript**: 유형 safety 방지합니다 런타임 오류
2. **Implement 적절한 오류 처리**: Use 사용자 정의 오류 클래스
3. **Validate 입력**: Use 라이브러리 같은 Zod 또는 Joi
4. **Use 환경 변수**: 절대 ~하지 않음 hardcode secrets
5. **Implement 로깅**: Use 구조화된 로깅 (Pino, Winston)
6. **Add 속도 제한**: Prevent abuse
7. **Use HTTPS**: 항상 에서 production
8. **Implement CORS 적절하게**: Don't use `*` 에서 production
9. **Use 종속성 인젝션**: Easier 테스트 및 유지보수
10. **Write 테스트합니다**: 단위, 통합, 및 E2E 테스트합니다
11. **Handle graceful shutdown**: Clean up 리소스
12. **Use 연결 풀링**: 위한 databases
13. **Implement health 확인합니다**: 위한 모니터링
14. **Use 압축**: Reduce 응답 size
15. **모니터 성능**: Use APM tools

## 테스트 패턴

See `javascript-testing-patterns` skill 위한 포괄적인 테스트 guidance.

## 리소스

- **Node.js 최선의 관행**: https://github.com/goldbergyoni/nodebestpractices
- **Express.js 가이드**: https://expressjs.com/en/guide/
- **Fastify 문서화**: https://www.fastify.io/docs/
- **TypeScript 노드 Starter**: https://github.com/microsoft/TypeScript-Node-Starter
