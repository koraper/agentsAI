---
name: typescript-advanced-types
description: 마스터 TypeScript's 고급 유형 시스템 포함하여 generics, conditional 유형, mapped 유형, 템플릿 literals, 및 utility 유형 위한 구축 유형-safe 애플리케이션. Use 때 implementing 복잡한 유형 logic, 생성하는 reusable 유형 utilities, 또는 보장하는 compile-시간 유형 safety 에서 TypeScript projects.
---

# TypeScript 고급 유형

포괄적인 guidance 위한 mastering TypeScript's 고급 유형 시스템 포함하여 generics, conditional 유형, mapped 유형, 템플릿 literal 유형, 및 utility 유형 위한 구축 강력한, 유형-safe 애플리케이션.

## 때 에 Use This Skill

- 구축 유형-safe 라이브러리 또는 프레임워크
- 생성하는 reusable 일반 컴포넌트
- Implementing 복잡한 유형 inference logic
- Designing 유형-safe API 클라이언트
- 구축 폼 검증 시스템
- 생성하는 강하게-typed 구성 객체
- Implementing 유형-safe 상태 관리
- Migrating JavaScript codebases 에 TypeScript

## 핵심 개념

### 1. Generics

**Purpose:** Create reusable, 유형-유연한 컴포넌트 동안 maintaining 유형 safety.

**기본 일반 함수:**
```typescript
function identity<T>(value: T): T {
  return value;
}

const num = identity<number>(42);        // Type: number
const str = identity<string>("hello");    // Type: string
const auto = identity(true);              // Type inferred: boolean
```

**일반 Constraints:**
```typescript
interface HasLength {
  length: number;
}

function logLength<T extends HasLength>(item: T): T {
  console.log(item.length);
  return item;
}

logLength("hello");           // OK: string has length
logLength([1, 2, 3]);         // OK: array has length
logLength({ length: 10 });    // OK: object has length
// logLength(42);             // Error: number has no length
```

**여러 유형 매개변수:**
```typescript
function merge<T, U>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 };
}

const merged = merge(
  { name: "John" },
  { age: 30 }
);
// Type: { name: string } & { age: number }
```

### 2. Conditional 유형

**Purpose:** Create 유형 것 depend 에 conditions, 가능하게 하는 정교한 유형 logic.

**기본 Conditional 유형:**
```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<string>;    // true
type B = IsString<number>;    // false
```

**Extracting 반환 유형:**
```typescript
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

function getUser() {
  return { id: 1, name: "John" };
}

type User = ReturnType<typeof getUser>;
// Type: { id: number; name: string; }
```

**Distributive Conditional 유형:**
```typescript
type ToArray<T> = T extends any ? T[] : never;

type StrOrNumArray = ToArray<string | number>;
// Type: string[] | number[]
```

**Nested Conditions:**
```typescript
type TypeName<T> =
  T extends string ? "string" :
  T extends number ? "number" :
  T extends boolean ? "boolean" :
  T extends undefined ? "undefined" :
  T extends Function ? "function" :
  "object";

type T1 = TypeName<string>;     // "string"
type T2 = TypeName<() => void>; // "function"
```

### 3. Mapped 유형

**Purpose:** Transform 기존 유형 에 의해 iterating over their 속성.

**기본 Mapped 유형:**
```typescript
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

interface User {
  id: number;
  name: string;
}

type ReadonlyUser = Readonly<User>;
// Type: { readonly id: number; readonly name: string; }
```

**선택적 속성:**
```typescript
type Partial<T> = {
  [P in keyof T]?: T[P];
};

type PartialUser = Partial<User>;
// Type: { id?: number; name?: string; }
```

**키 Remapping:**
```typescript
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
};

interface Person {
  name: string;
  age: number;
}

type PersonGetters = Getters<Person>;
// Type: { getName: () => string; getAge: () => number; }
```

**필터링 속성:**
```typescript
type PickByType<T, U> = {
  [K in keyof T as T[K] extends U ? K : never]: T[K]
};

interface Mixed {
  id: number;
  name: string;
  age: number;
  active: boolean;
}

type OnlyNumbers = PickByType<Mixed, number>;
// Type: { id: number; age: number; }
```

### 4. 템플릿 Literal 유형

**Purpose:** Create string-based 유형 와 함께 패턴 일치하는 및 변환.

**기본 템플릿 Literal:**
```typescript
type EventName = "click" | "focus" | "blur";
type EventHandler = `on${Capitalize<EventName>}`;
// Type: "onClick" | "onFocus" | "onBlur"
```

**String Manipulation:**
```typescript
type UppercaseGreeting = Uppercase<"hello">;  // "HELLO"
type LowercaseGreeting = Lowercase<"HELLO">;  // "hello"
type CapitalizedName = Capitalize<"john">;    // "John"
type UncapitalizedName = Uncapitalize<"John">; // "john"
```

**경로 구축:**
```typescript
type Path<T> = T extends object
  ? { [K in keyof T]: K extends string
      ? `${K}` | `${K}.${Path<T[K]>}`
      : never
    }[keyof T]
  : never;

interface Config {
  server: {
    host: string;
    port: number;
  };
  database: {
    url: string;
  };
}

type ConfigPath = Path<Config>;
// Type: "server" | "database" | "server.host" | "server.port" | "database.url"
```

### 5. Utility 유형

**구축된-에서 Utility 유형:**

```typescript
// Partial<T> - Make all properties optional
type PartialUser = Partial<User>;

// Required<T> - Make all properties required
type RequiredUser = Required<PartialUser>;

// Readonly<T> - Make all properties readonly
type ReadonlyUser = Readonly<User>;

// Pick<T, K> - Select specific properties
type UserName = Pick<User, "name" | "email">;

// Omit<T, K> - Remove specific properties
type UserWithoutPassword = Omit<User, "password">;

// Exclude<T, U> - Exclude types from union
type T1 = Exclude<"a" | "b" | "c", "a">;  // "b" | "c"

// Extract<T, U> - Extract types from union
type T2 = Extract<"a" | "b" | "c", "a" | "b">;  // "a" | "b"

// NonNullable<T> - Exclude null and undefined
type T3 = NonNullable<string | null | undefined>;  // string

// Record<K, T> - Create object type with keys K and values T
type PageInfo = Record<"home" | "about", { title: string }>;
```

## 고급 패턴

### 패턴 1: 유형-Safe 이벤트 Emitter

```typescript
type EventMap = {
  "user:created": { id: string; name: string };
  "user:updated": { id: string };
  "user:deleted": { id: string };
};

class TypedEventEmitter<T extends Record<string, any>> {
  private listeners: {
    [K in keyof T]?: Array<(data: T[K]) => void>;
  } = {};

  on<K extends keyof T>(event: K, callback: (data: T[K]) => void): void {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event]!.push(callback);
  }

  emit<K extends keyof T>(event: K, data: T[K]): void {
    const callbacks = this.listeners[event];
    if (callbacks) {
      callbacks.forEach(callback => callback(data));
    }
  }
}

const emitter = new TypedEventEmitter<EventMap>();

emitter.on("user:created", (data) => {
  console.log(data.id, data.name);  // Type-safe!
});

emitter.emit("user:created", { id: "1", name: "John" });
// emitter.emit("user:created", { id: "1" });  // Error: missing 'name'
```

### 패턴 2: 유형-Safe API 클라이언트

```typescript
type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE";

type EndpointConfig = {
  "/users": {
    GET: { response: User[] };
    POST: { body: { name: string; email: string }; response: User };
  };
  "/users/:id": {
    GET: { params: { id: string }; response: User };
    PUT: { params: { id: string }; body: Partial<User>; response: User };
    DELETE: { params: { id: string }; response: void };
  };
};

type ExtractParams<T> = T extends { params: infer P } ? P : never;
type ExtractBody<T> = T extends { body: infer B } ? B : never;
type ExtractResponse<T> = T extends { response: infer R } ? R : never;

class APIClient<Config extends Record<string, Record<HTTPMethod, any>>> {
  async request<
    Path extends keyof Config,
    Method extends keyof Config[Path]
  >(
    path: Path,
    method: Method,
    ...[options]: ExtractParams<Config[Path][Method]> extends never
      ? ExtractBody<Config[Path][Method]> extends never
        ? []
        : [{ body: ExtractBody<Config[Path][Method]> }]
      : [{
          params: ExtractParams<Config[Path][Method]>;
          body?: ExtractBody<Config[Path][Method]>;
        }]
  ): Promise<ExtractResponse<Config[Path][Method]>> {
    // Implementation here
    return {} as any;
  }
}

const api = new APIClient<EndpointConfig>();

// Type-safe API calls
const users = await api.request("/users", "GET");
// Type: User[]

const newUser = await api.request("/users", "POST", {
  body: { name: "John", email: "john@example.com" }
});
// Type: User

const user = await api.request("/users/:id", "GET", {
  params: { id: "123" }
});
// Type: User
```

### 패턴 3: 빌더 패턴 와 함께 유형 Safety

```typescript
type BuilderState<T> = {
  [K in keyof T]: T[K] | undefined;
};

type RequiredKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? never : K;
}[keyof T];

type OptionalKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? K : never;
}[keyof T];

type IsComplete<T, S> =
  RequiredKeys<T> extends keyof S
    ? S[RequiredKeys<T>] extends undefined
      ? false
      : true
    : false;

class Builder<T, S extends BuilderState<T> = {}> {
  private state: S = {} as S;

  set<K extends keyof T>(
    key: K,
    value: T[K]
  ): Builder<T, S & Record<K, T[K]>> {
    this.state[key] = value;
    return this as any;
  }

  build(
    this: IsComplete<T, S> extends true ? this : never
  ): T {
    return this.state as T;
  }
}

interface User {
  id: string;
  name: string;
  email: string;
  age?: number;
}

const builder = new Builder<User>();

const user = builder
  .set("id", "1")
  .set("name", "John")
  .set("email", "john@example.com")
  .build();  // OK: all required fields set

// const incomplete = builder
//   .set("id", "1")
//   .build();  // Error: missing required fields
```

### 패턴 4: Deep Readonly/부분

```typescript
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object
    ? T[P] extends Function
      ? T[P]
      : DeepReadonly<T[P]>
    : T[P];
};

type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object
    ? T[P] extends Array<infer U>
      ? Array<DeepPartial<U>>
      : DeepPartial<T[P]>
    : T[P];
};

interface Config {
  server: {
    host: string;
    port: number;
    ssl: {
      enabled: boolean;
      cert: string;
    };
  };
  database: {
    url: string;
    pool: {
      min: number;
      max: number;
    };
  };
}

type ReadonlyConfig = DeepReadonly<Config>;
// All nested properties are readonly

type PartialConfig = DeepPartial<Config>;
// All nested properties are optional
```

### 패턴 5: 유형-Safe 폼 검증

```typescript
type ValidationRule<T> = {
  validate: (value: T) => boolean;
  message: string;
};

type FieldValidation<T> = {
  [K in keyof T]?: ValidationRule<T[K]>[];
};

type ValidationErrors<T> = {
  [K in keyof T]?: string[];
};

class FormValidator<T extends Record<string, any>> {
  constructor(private rules: FieldValidation<T>) {}

  validate(data: T): ValidationErrors<T> | null {
    const errors: ValidationErrors<T> = {};
    let hasErrors = false;

    for (const key in this.rules) {
      const fieldRules = this.rules[key];
      const value = data[key];

      if (fieldRules) {
        const fieldErrors: string[] = [];

        for (const rule of fieldRules) {
          if (!rule.validate(value)) {
            fieldErrors.push(rule.message);
          }
        }

        if (fieldErrors.length > 0) {
          errors[key] = fieldErrors;
          hasErrors = true;
        }
      }
    }

    return hasErrors ? errors : null;
  }
}

interface LoginForm {
  email: string;
  password: string;
}

const validator = new FormValidator<LoginForm>({
  email: [
    {
      validate: (v) => v.includes("@"),
      message: "Email must contain @"
    },
    {
      validate: (v) => v.length > 0,
      message: "Email is required"
    }
  ],
  password: [
    {
      validate: (v) => v.length >= 8,
      message: "Password must be at least 8 characters"
    }
  ]
});

const errors = validator.validate({
  email: "invalid",
  password: "short"
});
// Type: { email?: string[]; password?: string[]; } | null
```

### 패턴 6: 식별된 Unions

```typescript
type Success<T> = {
  status: "success";
  data: T;
};

type Error = {
  status: "error";
  error: string;
};

type Loading = {
  status: "loading";
};

type AsyncState<T> = Success<T> | Error | Loading;

function handleState<T>(state: AsyncState<T>): void {
  switch (state.status) {
    case "success":
      console.log(state.data);  // Type: T
      break;
    case "error":
      console.log(state.error);  // Type: string
      break;
    case "loading":
      console.log("Loading...");
      break;
  }
}

// Type-safe state machine
type State =
  | { type: "idle" }
  | { type: "fetching"; requestId: string }
  | { type: "success"; data: any }
  | { type: "error"; error: Error };

type Event =
  | { type: "FETCH"; requestId: string }
  | { type: "SUCCESS"; data: any }
  | { type: "ERROR"; error: Error }
  | { type: "RESET" };

function reducer(state: State, event: Event): State {
  switch (state.type) {
    case "idle":
      return event.type === "FETCH"
        ? { type: "fetching", requestId: event.requestId }
        : state;
    case "fetching":
      if (event.type === "SUCCESS") {
        return { type: "success", data: event.data };
      }
      if (event.type === "ERROR") {
        return { type: "error", error: event.error };
      }
      return state;
    case "success":
    case "error":
      return event.type === "RESET" ? { type: "idle" } : state;
  }
}
```

## 유형 Inference Techniques

### 1. Infer Keyword

```typescript
// Extract array element type
type ElementType<T> = T extends (infer U)[] ? U : never;

type NumArray = number[];
type Num = ElementType<NumArray>;  // number

// Extract promise type
type PromiseType<T> = T extends Promise<infer U> ? U : never;

type AsyncNum = PromiseType<Promise<number>>;  // number

// Extract function parameters
type Parameters<T> = T extends (...args: infer P) => any ? P : never;

function foo(a: string, b: number) {}
type FooParams = Parameters<typeof foo>;  // [string, number]
```

### 2. 유형 Guards

```typescript
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function isArrayOf<T>(
  value: unknown,
  guard: (item: unknown) => item is T
): value is T[] {
  return Array.isArray(value) && value.every(guard);
}

const data: unknown = ["a", "b", "c"];

if (isArrayOf(data, isString)) {
  data.forEach(s => s.toUpperCase());  // Type: string[]
}
```

### 3. Assertion 함수

```typescript
function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") {
    throw new Error("Not a string");
  }
}

function processValue(value: unknown) {
  assertIsString(value);
  // value is now typed as string
  console.log(value.toUpperCase());
}
```

## 최선의 관행

1. **Use `unknown` over `any`**: Enforce 유형 확인
2. **Prefer `interface` 위한 객체 shapes**: 더 나은 오류 메시지
3. **Use `type` 위한 unions 및 복잡한 유형**: More 유연한
4. **Leverage 유형 inference**: Let TypeScript infer 때 possible
5. **Create helper 유형**: 빌드 reusable 유형 utilities
6. **Use const assertions**: Preserve literal 유형
7. **Avoid 유형 assertions**: Use 유형 guards instead
8. **Document 복잡한 유형**: Add JSDoc comments
9. **Use strict 최빈값**: Enable 모든 strict 컴파일러 options
10. **Test your 유형**: Use 유형 테스트합니다 에 verify 유형 behavior

## 유형 테스트

```typescript
// Type assertion tests
type AssertEqual<T, U> =
  [T] extends [U]
    ? [U] extends [T]
      ? true
      : false
    : false;

type Test1 = AssertEqual<string, string>;        // true
type Test2 = AssertEqual<string, number>;        // false
type Test3 = AssertEqual<string | number, string>; // false

// Expect error helper
type ExpectError<T extends never> = T;

// Example usage
type ShouldError = ExpectError<AssertEqual<string, number>>;
```

## 일반적인 Pitfalls

1. **Over-사용하여 `any`**: Defeats the purpose of TypeScript
2. **Ignoring strict null 확인합니다**: Can 리드 에 런타임 오류
3. **또한 복잡한 유형**: Can slow down 컴파일
4. **Not 사용하여 식별된 unions**: Misses 유형 narrowing opportunities
5. **Forgetting readonly modifiers**: 허용합니다 unintended mutations
6. **Circular 유형 참조**: Can cause 컴파일러 오류
7. **Not 처리 엣지 cases**: 같은 빈 배열 또는 null 값

## 성능 Considerations

- Avoid 깊이 nested conditional 유형
- Use 간단한 유형 때 possible
- 캐시 복잡한 유형 computations
- Limit 재귀 depth 에서 recursive 유형
- Use 빌드 tools 에 skip 유형 확인 에서 production

## 리소스

- **TypeScript Handbook**: https://www.typescriptlang.org/docs/handbook/
- **유형 Challenges**: https://github.com/type-challenges/type-challenges
- **TypeScript Deep Dive**: https://basarat.gitbook.io/typescript/
- **Effective TypeScript**: Book 에 의해 Dan Vanderkam
