---
name: auth-implementation-patterns
description: 마스터 인증 및 인가 패턴 포함하여 JWT, OAuth2, 세션 관리, 및 RBAC 에 빌드 secure, scalable access control 시스템. Use 때 implementing auth 시스템, securing APIs, 또는 디버깅 security 이슈.
---

# 인증 & 인가 구현 패턴

빌드 secure, scalable 인증 및 인가 시스템 사용하여 산업-표준 패턴 및 현대적인 최선의 관행.

## 때 에 Use This Skill

- Implementing 사용자 인증 시스템
- Securing REST 또는 GraphQL APIs
- Adding OAuth2/social login
- Implementing role-based access control (RBAC)
- Designing 세션 관리
- Migrating 인증 시스템
- 디버깅 auth 이슈
- Implementing SSO 또는 multi-tenancy

## 핵심 개념

### 1. 인증 vs 인가

**인증 (AuthN)**: 누구 are you?
- Verifying 아이덴티티 (username/password, OAuth, biometrics)
- Issuing 자격 증명 (세션, 토큰)
- Managing login/logout

**인가 (AuthZ)**: 무엇 can you do?
- 권한 확인
- Role-based access control (RBAC)
- 리소스 ownership 검증
- 정책 enforcement

### 2. 인증 Strategies

**세션-Based:**
- 서버 저장합니다 세션 상태
- 세션 ID 에서 쿠키
- 전통적인, 간단한, stateful

**토큰-Based (JWT):**
- Stateless, self-contained
- 확장합니다 horizontally
- Can store claims

**OAuth2/OpenID Connect:**
- Delegate 인증
- Social login (Google, GitHub)
- 엔터프라이즈 SSO

## JWT 인증

### 패턴 1: JWT 구현

```typescript
// JWT structure: header.payload.signature
import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';

interface JWTPayload {
    userId: string;
    email: string;
    role: string;
    iat: number;
    exp: number;
}

// Generate JWT
function generateTokens(userId: string, email: string, role: string) {
    const accessToken = jwt.sign(
        { userId, email, role },
        process.env.JWT_SECRET!,
        { expiresIn: '15m' }  // Short-lived
    );

    const refreshToken = jwt.sign(
        { userId },
        process.env.JWT_REFRESH_SECRET!,
        { expiresIn: '7d' }  // Long-lived
    );

    return { accessToken, refreshToken };
}

// Verify JWT
function verifyToken(token: string): JWTPayload {
    try {
        return jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload;
    } catch (error) {
        if (error instanceof jwt.TokenExpiredError) {
            throw new Error('Token expired');
        }
        if (error instanceof jwt.JsonWebTokenError) {
            throw new Error('Invalid token');
        }
        throw error;
    }
}

// Middleware
function authenticate(req: Request, res: Response, next: NextFunction) {
    const authHeader = req.headers.authorization;
    if (!authHeader?.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'No token provided' });
    }

    const token = authHeader.substring(7);
    try {
        const payload = verifyToken(token);
        req.user = payload;  // Attach user to request
        next();
    } catch (error) {
        return res.status(401).json({ error: 'Invalid token' });
    }
}

// Usage
app.get('/api/profile', authenticate, (req, res) => {
    res.json({ user: req.user });
});
```

### 패턴 2: Refresh 토큰 흐름

```typescript
interface StoredRefreshToken {
    token: string;
    userId: string;
    expiresAt: Date;
    createdAt: Date;
}

class RefreshTokenService {
    // Store refresh token in database
    async storeRefreshToken(userId: string, refreshToken: string) {
        const expiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
        await db.refreshTokens.create({
            token: await hash(refreshToken),  // Hash before storing
            userId,
            expiresAt,
        });
    }

    // Refresh access token
    async refreshAccessToken(refreshToken: string) {
        // Verify refresh token
        let payload;
        try {
            payload = jwt.verify(
                refreshToken,
                process.env.JWT_REFRESH_SECRET!
            ) as { userId: string };
        } catch {
            throw new Error('Invalid refresh token');
        }

        // Check if token exists in database
        const storedToken = await db.refreshTokens.findOne({
            where: {
                token: await hash(refreshToken),
                userId: payload.userId,
                expiresAt: { $gt: new Date() },
            },
        });

        if (!storedToken) {
            throw new Error('Refresh token not found or expired');
        }

        // Get user
        const user = await db.users.findById(payload.userId);
        if (!user) {
            throw new Error('User not found');
        }

        // Generate new access token
        const accessToken = jwt.sign(
            { userId: user.id, email: user.email, role: user.role },
            process.env.JWT_SECRET!,
            { expiresIn: '15m' }
        );

        return { accessToken };
    }

    // Revoke refresh token (logout)
    async revokeRefreshToken(refreshToken: string) {
        await db.refreshTokens.deleteOne({
            token: await hash(refreshToken),
        });
    }

    // Revoke all user tokens (logout all devices)
    async revokeAllUserTokens(userId: string) {
        await db.refreshTokens.deleteMany({ userId });
    }
}

// API endpoints
app.post('/api/auth/refresh', async (req, res) => {
    const { refreshToken } = req.body;
    try {
        const { accessToken } = await refreshTokenService
            .refreshAccessToken(refreshToken);
        res.json({ accessToken });
    } catch (error) {
        res.status(401).json({ error: 'Invalid refresh token' });
    }
});

app.post('/api/auth/logout', authenticate, async (req, res) => {
    const { refreshToken } = req.body;
    await refreshTokenService.revokeRefreshToken(refreshToken);
    res.json({ message: 'Logged out successfully' });
});
```

## 세션-Based 인증

### 패턴 1: Express 세션

```typescript
import session from 'express-session';
import RedisStore from 'connect-redis';
import { createClient } from 'redis';

// Setup Redis for session storage
const redisClient = createClient({
    url: process.env.REDIS_URL,
});
await redisClient.connect();

app.use(
    session({
        store: new RedisStore({ client: redisClient }),
        secret: process.env.SESSION_SECRET!,
        resave: false,
        saveUninitialized: false,
        cookie: {
            secure: process.env.NODE_ENV === 'production',  // HTTPS only
            httpOnly: true,  // No JavaScript access
            maxAge: 24 * 60 * 60 * 1000,  // 24 hours
            sameSite: 'strict',  // CSRF protection
        },
    })
);

// Login
app.post('/api/auth/login', async (req, res) => {
    const { email, password } = req.body;

    const user = await db.users.findOne({ email });
    if (!user || !(await verifyPassword(password, user.passwordHash))) {
        return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Store user in session
    req.session.userId = user.id;
    req.session.role = user.role;

    res.json({ user: { id: user.id, email: user.email, role: user.role } });
});

// Session middleware
function requireAuth(req: Request, res: Response, next: NextFunction) {
    if (!req.session.userId) {
        return res.status(401).json({ error: 'Not authenticated' });
    }
    next();
}

// Protected route
app.get('/api/profile', requireAuth, async (req, res) => {
    const user = await db.users.findById(req.session.userId);
    res.json({ user });
});

// Logout
app.post('/api/auth/logout', (req, res) => {
    req.session.destroy((err) => {
        if (err) {
            return res.status(500).json({ error: 'Logout failed' });
        }
        res.clearCookie('connect.sid');
        res.json({ message: 'Logged out successfully' });
    });
});
```

## OAuth2 / Social Login

### 패턴 1: OAuth2 와 함께 Passport.js

```typescript
import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';
import { Strategy as GitHubStrategy } from 'passport-github2';

// Google OAuth
passport.use(
    new GoogleStrategy(
        {
            clientID: process.env.GOOGLE_CLIENT_ID!,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
            callbackURL: '/api/auth/google/callback',
        },
        async (accessToken, refreshToken, profile, done) => {
            try {
                // Find or create user
                let user = await db.users.findOne({
                    googleId: profile.id,
                });

                if (!user) {
                    user = await db.users.create({
                        googleId: profile.id,
                        email: profile.emails?.[0]?.value,
                        name: profile.displayName,
                        avatar: profile.photos?.[0]?.value,
                    });
                }

                return done(null, user);
            } catch (error) {
                return done(error, undefined);
            }
        }
    )
);

// Routes
app.get('/api/auth/google', passport.authenticate('google', {
    scope: ['profile', 'email'],
}));

app.get(
    '/api/auth/google/callback',
    passport.authenticate('google', { session: false }),
    (req, res) => {
        // Generate JWT
        const tokens = generateTokens(req.user.id, req.user.email, req.user.role);
        // Redirect to frontend with token
        res.redirect(`${process.env.FRONTEND_URL}/auth/callback?token=${tokens.accessToken}`);
    }
);
```

## 인가 패턴

### 패턴 1: Role-Based Access Control (RBAC)

```typescript
enum Role {
    USER = 'user',
    MODERATOR = 'moderator',
    ADMIN = 'admin',
}

const roleHierarchy: Record<Role, Role[]> = {
    [Role.ADMIN]: [Role.ADMIN, Role.MODERATOR, Role.USER],
    [Role.MODERATOR]: [Role.MODERATOR, Role.USER],
    [Role.USER]: [Role.USER],
};

function hasRole(userRole: Role, requiredRole: Role): boolean {
    return roleHierarchy[userRole].includes(requiredRole);
}

// Middleware
function requireRole(...roles: Role[]) {
    return (req: Request, res: Response, next: NextFunction) => {
        if (!req.user) {
            return res.status(401).json({ error: 'Not authenticated' });
        }

        if (!roles.some(role => hasRole(req.user.role, role))) {
            return res.status(403).json({ error: 'Insufficient permissions' });
        }

        next();
    };
}

// Usage
app.delete('/api/users/:id',
    authenticate,
    requireRole(Role.ADMIN),
    async (req, res) => {
        // Only admins can delete users
        await db.users.delete(req.params.id);
        res.json({ message: 'User deleted' });
    }
);
```

### 패턴 2: 권한-Based Access Control

```typescript
enum Permission {
    READ_USERS = 'read:users',
    WRITE_USERS = 'write:users',
    DELETE_USERS = 'delete:users',
    READ_POSTS = 'read:posts',
    WRITE_POSTS = 'write:posts',
}

const rolePermissions: Record<Role, Permission[]> = {
    [Role.USER]: [Permission.READ_POSTS, Permission.WRITE_POSTS],
    [Role.MODERATOR]: [
        Permission.READ_POSTS,
        Permission.WRITE_POSTS,
        Permission.READ_USERS,
    ],
    [Role.ADMIN]: Object.values(Permission),
};

function hasPermission(userRole: Role, permission: Permission): boolean {
    return rolePermissions[userRole]?.includes(permission) ?? false;
}

function requirePermission(...permissions: Permission[]) {
    return (req: Request, res: Response, next: NextFunction) => {
        if (!req.user) {
            return res.status(401).json({ error: 'Not authenticated' });
        }

        const hasAllPermissions = permissions.every(permission =>
            hasPermission(req.user.role, permission)
        );

        if (!hasAllPermissions) {
            return res.status(403).json({ error: 'Insufficient permissions' });
        }

        next();
    };
}

// Usage
app.get('/api/users',
    authenticate,
    requirePermission(Permission.READ_USERS),
    async (req, res) => {
        const users = await db.users.findAll();
        res.json({ users });
    }
);
```

### 패턴 3: 리소스 Ownership

```typescript
// Check if user owns resource
async function requireOwnership(
    resourceType: 'post' | 'comment',
    resourceIdParam: string = 'id'
) {
    return async (req: Request, res: Response, next: NextFunction) => {
        if (!req.user) {
            return res.status(401).json({ error: 'Not authenticated' });
        }

        const resourceId = req.params[resourceIdParam];

        // Admins can access anything
        if (req.user.role === Role.ADMIN) {
            return next();
        }

        // Check ownership
        let resource;
        if (resourceType === 'post') {
            resource = await db.posts.findById(resourceId);
        } else if (resourceType === 'comment') {
            resource = await db.comments.findById(resourceId);
        }

        if (!resource) {
            return res.status(404).json({ error: 'Resource not found' });
        }

        if (resource.userId !== req.user.userId) {
            return res.status(403).json({ error: 'Not authorized' });
        }

        next();
    };
}

// Usage
app.put('/api/posts/:id',
    authenticate,
    requireOwnership('post'),
    async (req, res) => {
        // User can only update their own posts
        const post = await db.posts.update(req.params.id, req.body);
        res.json({ post });
    }
);
```

## Security 최선의 관행

### 패턴 1: Password Security

```typescript
import bcrypt from 'bcrypt';
import { z } from 'zod';

// Password validation schema
const passwordSchema = z.string()
    .min(12, 'Password must be at least 12 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[a-z]/, 'Password must contain lowercase letter')
    .regex(/[0-9]/, 'Password must contain number')
    .regex(/[^A-Za-z0-9]/, 'Password must contain special character');

// Hash password
async function hashPassword(password: string): Promise<string> {
    const saltRounds = 12;  // 2^12 iterations
    return bcrypt.hash(password, saltRounds);
}

// Verify password
async function verifyPassword(
    password: string,
    hash: string
): Promise<boolean> {
    return bcrypt.compare(password, hash);
}

// Registration with password validation
app.post('/api/auth/register', async (req, res) => {
    try {
        const { email, password } = req.body;

        // Validate password
        passwordSchema.parse(password);

        // Check if user exists
        const existingUser = await db.users.findOne({ email });
        if (existingUser) {
            return res.status(400).json({ error: 'Email already registered' });
        }

        // Hash password
        const passwordHash = await hashPassword(password);

        // Create user
        const user = await db.users.create({
            email,
            passwordHash,
        });

        // Generate tokens
        const tokens = generateTokens(user.id, user.email, user.role);

        res.status(201).json({
            user: { id: user.id, email: user.email },
            ...tokens,
        });
    } catch (error) {
        if (error instanceof z.ZodError) {
            return res.status(400).json({ error: error.errors[0].message });
        }
        res.status(500).json({ error: 'Registration failed' });
    }
});
```

### 패턴 2: 속도 제한

```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';

// Login rate limiter
const loginLimiter = rateLimit({
    store: new RedisStore({ client: redisClient }),
    windowMs: 15 * 60 * 1000,  // 15 minutes
    max: 5,  // 5 attempts
    message: 'Too many login attempts, please try again later',
    standardHeaders: true,
    legacyHeaders: false,
});

// API rate limiter
const apiLimiter = rateLimit({
    windowMs: 60 * 1000,  // 1 minute
    max: 100,  // 100 requests per minute
    standardHeaders: true,
});

// Apply to routes
app.post('/api/auth/login', loginLimiter, async (req, res) => {
    // Login logic
});

app.use('/api/', apiLimiter);
```

## 최선의 관행

1. **절대 ~하지 않음 Store Plain Passwords**: 항상 해시 와 함께 bcrypt/argon2
2. **Use HTTPS**: Encrypt 데이터 에서 transit
3. **Short-Lived Access 토큰**: 15-30 minutes max
4. **Secure 쿠키**: httpOnly, secure, sameSite flags
5. **Validate 모든 입력**: Email format, password strength
6. **Rate Limit Auth 엔드포인트**: Prevent brute force 공격
7. **Implement CSRF 보호**: 위한 세션-based auth
8. **Rotate Secrets 정기적으로**: JWT secrets, 세션 secrets
9. **Log Security 이벤트**: Login attempts, 실패 auth
10. **Use MFA 때 Possible**: Extra security 레이어

## 일반적인 Pitfalls

- **약한 Passwords**: Enforce 강한 password 정책
- **JWT 에서 localStorage**: Vulnerable 에 XSS, use httpOnly 쿠키
- **아니요 토큰 Expiration**: 토큰 should expire
- **클라이언트-Side Auth 확인합니다 오직**: 항상 validate 서버-side
- **Insecure Password Reset**: Use secure 토큰 와 함께 expiration
- **아니요 속도 제한**: Vulnerable 에 brute force
- **Trusting 클라이언트 데이터**: 항상 validate 에 서버

## 리소스

- **참조/jwt-최선의-관행.md**: JWT 구현 가이드
- **참조/oauth2-흐릅니다.md**: OAuth2 흐름 다이어그램 및 예제
- **참조/세션-security.md**: Secure 세션 관리
- **자산/auth-security-checklist.md**: Security review checklist
- **자산/password-정책-템플릿.md**: Password 요구사항 템플릿
- **스크립트/토큰-검증기.ts**: JWT 검증 utility
