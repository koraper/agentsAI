---
name: modern-javascript-patterns
description: 마스터 ES6+ 기능 포함하여 비동기/await, destructuring, 분산 operators, arrow 함수, promises, 모듈, iterators, generators, 및 기능적인 programming 패턴 위한 작성 clean, efficient JavaScript 코드. Use 때 리팩토링 레거시 코드, implementing 현대적인 패턴, 또는 optimizing JavaScript 애플리케이션.
---

# 현대적인 JavaScript 패턴

포괄적인 가이드 위한 mastering 현대적인 JavaScript (ES6+) 기능, 기능적인 programming 패턴, 및 최선의 관행 위한 작성 clean, maintainable, 및 performant 코드.

## 때 에 Use This Skill

- 리팩토링 레거시 JavaScript 에 현대적인 구문
- Implementing 기능적인 programming 패턴
- Optimizing JavaScript 성능
- 작성 maintainable 및 readable 코드
- 작업 와 함께 asynchronous 작업
- 구축 현대적인 web 애플리케이션
- Migrating 에서 callbacks 에 Promises/비동기-await
- Implementing 데이터 변환 파이프라인

## ES6+ 핵심 기능

### 1. Arrow 함수

**구문 및 Use Cases:**
```javascript
// Traditional function
function add(a, b) {
  return a + b;
}

// Arrow function
const add = (a, b) => a + b;

// Single parameter (parentheses optional)
const double = x => x * 2;

// No parameters
const getRandom = () => Math.random();

// Multiple statements (need curly braces)
const processUser = user => {
  const normalized = user.name.toLowerCase();
  return { ...user, name: normalized };
};

// Returning objects (wrap in parentheses)
const createUser = (name, age) => ({ name, age });
```

**Lexical 'this' 바인딩:**
```javascript
class Counter {
  constructor() {
    this.count = 0;
  }

  // Arrow function preserves 'this' context
  increment = () => {
    this.count++;
  };

  // Traditional function loses 'this' in callbacks
  incrementTraditional() {
    setTimeout(function() {
      this.count++;  // 'this' is undefined
    }, 1000);
  }

  // Arrow function maintains 'this'
  incrementArrow() {
    setTimeout(() => {
      this.count++;  // 'this' refers to Counter instance
    }, 1000);
  }
}
```

### 2. Destructuring

**객체 Destructuring:**
```javascript
const user = {
  id: 1,
  name: 'John Doe',
  email: 'john@example.com',
  address: {
    city: 'New York',
    country: 'USA'
  }
};

// Basic destructuring
const { name, email } = user;

// Rename variables
const { name: userName, email: userEmail } = user;

// Default values
const { age = 25 } = user;

// Nested destructuring
const { address: { city, country } } = user;

// Rest operator
const { id, ...userWithoutId } = user;

// Function parameters
function greet({ name, age = 18 }) {
  console.log(`Hello ${name}, you are ${age}`);
}
greet(user);
```

**배열 Destructuring:**
```javascript
const numbers = [1, 2, 3, 4, 5];

// Basic destructuring
const [first, second] = numbers;

// Skip elements
const [, , third] = numbers;

// Rest operator
const [head, ...tail] = numbers;

// Swapping variables
let a = 1, b = 2;
[a, b] = [b, a];

// Function return values
function getCoordinates() {
  return [10, 20];
}
const [x, y] = getCoordinates();

// Default values
const [one, two, three = 0] = [1, 2];
```

### 3. 분산 및 Rest Operators

**분산 운영자:**
```javascript
// Array spreading
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2];

// Object spreading
const defaults = { theme: 'dark', lang: 'en' };
const userPrefs = { theme: 'light' };
const settings = { ...defaults, ...userPrefs };

// Function arguments
const numbers = [1, 2, 3];
Math.max(...numbers);

// Copying arrays/objects (shallow copy)
const copy = [...arr1];
const objCopy = { ...user };

// Adding items immutably
const newArr = [...arr1, 4, 5];
const newObj = { ...user, age: 30 };
```

**Rest 매개변수:**
```javascript
// Collect function arguments
function sum(...numbers) {
  return numbers.reduce((total, num) => total + num, 0);
}
sum(1, 2, 3, 4, 5);

// With regular parameters
function greet(greeting, ...names) {
  return `${greeting} ${names.join(', ')}`;
}
greet('Hello', 'John', 'Jane', 'Bob');

// Object rest
const { id, ...userData } = user;

// Array rest
const [first, ...rest] = [1, 2, 3, 4, 5];
```

### 4. 템플릿 Literals

```javascript
// Basic usage
const name = 'John';
const greeting = `Hello, ${name}!`;

// Multi-line strings
const html = `
  <div>
    <h1>${title}</h1>
    <p>${content}</p>
  </div>
`;

// Expression evaluation
const price = 19.99;
const total = `Total: $${(price * 1.2).toFixed(2)}`;

// Tagged template literals
function highlight(strings, ...values) {
  return strings.reduce((result, str, i) => {
    const value = values[i] || '';
    return result + str + `<mark>${value}</mark>`;
  }, '');
}

const name = 'John';
const age = 30;
const html = highlight`Name: ${name}, Age: ${age}`;
// Output: "Name: <mark>John</mark>, Age: <mark>30</mark>"
```

### 5. 향상된 객체 Literals

```javascript
const name = 'John';
const age = 30;

// Shorthand property names
const user = { name, age };

// Shorthand method names
const calculator = {
  add(a, b) {
    return a + b;
  },
  subtract(a, b) {
    return a - b;
  }
};

// Computed property names
const field = 'email';
const user = {
  name: 'John',
  [field]: 'john@example.com',
  [`get${field.charAt(0).toUpperCase()}${field.slice(1)}`]() {
    return this[field];
  }
};

// Dynamic property creation
const createUser = (name, ...props) => {
  return props.reduce((user, [key, value]) => ({
    ...user,
    [key]: value
  }), { name });
};

const user = createUser('John', ['age', 30], ['email', 'john@example.com']);
```

## Asynchronous 패턴

### 1. Promises

**생성하는 및 사용하여 Promises:**
```javascript
// Creating a promise
const fetchUser = (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id > 0) {
        resolve({ id, name: 'John' });
      } else {
        reject(new Error('Invalid ID'));
      }
    }, 1000);
  });
};

// Using promises
fetchUser(1)
  .then(user => console.log(user))
  .catch(error => console.error(error))
  .finally(() => console.log('Done'));

// Chaining promises
fetchUser(1)
  .then(user => fetchUserPosts(user.id))
  .then(posts => processPosts(posts))
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

**프로미스 Combinators:**
```javascript
// Promise.all - Wait for all promises
const promises = [
  fetchUser(1),
  fetchUser(2),
  fetchUser(3)
];

Promise.all(promises)
  .then(users => console.log(users))
  .catch(error => console.error('At least one failed:', error));

// Promise.allSettled - Wait for all, regardless of outcome
Promise.allSettled(promises)
  .then(results => {
    results.forEach(result => {
      if (result.status === 'fulfilled') {
        console.log('Success:', result.value);
      } else {
        console.log('Error:', result.reason);
      }
    });
  });

// Promise.race - First to complete
Promise.race(promises)
  .then(winner => console.log('First:', winner))
  .catch(error => console.error(error));

// Promise.any - First to succeed
Promise.any(promises)
  .then(first => console.log('First success:', first))
  .catch(error => console.error('All failed:', error));
```

### 2. 비동기/await

**기본 Usage:**
```javascript
// Async function always returns a Promise
async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`);
  const user = await response.json();
  return user;
}

// Error handling with try/catch
async function getUserData(id) {
  try {
    const user = await fetchUser(id);
    const posts = await fetchUserPosts(user.id);
    return { user, posts };
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
}

// Sequential vs Parallel execution
async function sequential() {
  const user1 = await fetchUser(1);  // Wait
  const user2 = await fetchUser(2);  // Then wait
  return [user1, user2];
}

async function parallel() {
  const [user1, user2] = await Promise.all([
    fetchUser(1),
    fetchUser(2)
  ]);
  return [user1, user2];
}
```

**고급 패턴:**
```javascript
// Async IIFE
(async () => {
  const result = await someAsyncOperation();
  console.log(result);
})();

// Async iteration
async function processUsers(userIds) {
  for (const id of userIds) {
    const user = await fetchUser(id);
    await processUser(user);
  }
}

// Top-level await (ES2022)
const config = await fetch('/config.json').then(r => r.json());

// Retry logic
async function fetchWithRetry(url, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fetch(url);
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}

// Timeout wrapper
async function withTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Timeout')), ms)
  );
  return Promise.race([promise, timeout]);
}
```

## 기능적인 Programming 패턴

### 1. 배열 메서드

**맵, 필터, Reduce:**
```javascript
const users = [
  { id: 1, name: 'John', age: 30, active: true },
  { id: 2, name: 'Jane', age: 25, active: false },
  { id: 3, name: 'Bob', age: 35, active: true }
];

// Map - Transform array
const names = users.map(user => user.name);
const upperNames = users.map(user => user.name.toUpperCase());

// Filter - Select elements
const activeUsers = users.filter(user => user.active);
const adults = users.filter(user => user.age >= 18);

// Reduce - Aggregate data
const totalAge = users.reduce((sum, user) => sum + user.age, 0);
const avgAge = totalAge / users.length;

// Group by property
const byActive = users.reduce((groups, user) => {
  const key = user.active ? 'active' : 'inactive';
  return {
    ...groups,
    [key]: [...(groups[key] || []), user]
  };
}, {});

// Chaining methods
const result = users
  .filter(user => user.active)
  .map(user => user.name)
  .sort()
  .join(', ');
```

**고급 배열 메서드:**
```javascript
// Find - First matching element
const user = users.find(u => u.id === 2);

// FindIndex - Index of first match
const index = users.findIndex(u => u.name === 'Jane');

// Some - At least one matches
const hasActive = users.some(u => u.active);

// Every - All match
const allAdults = users.every(u => u.age >= 18);

// FlatMap - Map and flatten
const userTags = [
  { name: 'John', tags: ['admin', 'user'] },
  { name: 'Jane', tags: ['user'] }
];
const allTags = userTags.flatMap(u => u.tags);

// From - Create array from iterable
const str = 'hello';
const chars = Array.from(str);
const numbers = Array.from({ length: 5 }, (_, i) => i + 1);

// Of - Create array from arguments
const arr = Array.of(1, 2, 3);
```

### 2. Higher-순서 함수

**함수 처럼 인수:**
```javascript
// Custom forEach
function forEach(array, callback) {
  for (let i = 0; i < array.length; i++) {
    callback(array[i], i, array);
  }
}

// Custom map
function map(array, transform) {
  const result = [];
  for (const item of array) {
    result.push(transform(item));
  }
  return result;
}

// Custom filter
function filter(array, predicate) {
  const result = [];
  for (const item of array) {
    if (predicate(item)) {
      result.push(item);
    }
  }
  return result;
}
```

**함수 Returning 함수:**
```javascript
// Currying
const multiply = a => b => a * b;
const double = multiply(2);
const triple = multiply(3);

console.log(double(5));  // 10
console.log(triple(5));  // 15

// Partial application
function partial(fn, ...args) {
  return (...moreArgs) => fn(...args, ...moreArgs);
}

const add = (a, b, c) => a + b + c;
const add5 = partial(add, 5);
console.log(add5(3, 2));  // 10

// Memoization
function memoize(fn) {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

const fibonacci = memoize((n) => {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});
```

### 3. Composition 및 파이핑

```javascript
// Function composition
const compose = (...fns) => x =>
  fns.reduceRight((acc, fn) => fn(acc), x);

const pipe = (...fns) => x =>
  fns.reduce((acc, fn) => fn(acc), x);

// Example usage
const addOne = x => x + 1;
const double = x => x * 2;
const square = x => x * x;

const composed = compose(square, double, addOne);
console.log(composed(3));  // ((3 + 1) * 2)^2 = 64

const piped = pipe(addOne, double, square);
console.log(piped(3));  // ((3 + 1) * 2)^2 = 64

// Practical example
const processUser = pipe(
  user => ({ ...user, name: user.name.trim() }),
  user => ({ ...user, email: user.email.toLowerCase() }),
  user => ({ ...user, age: parseInt(user.age) })
);

const user = processUser({
  name: '  John  ',
  email: 'JOHN@EXAMPLE.COM',
  age: '30'
});
```

### 4. Pure 함수 및 Immutability

```javascript
// Impure function (modifies input)
function addItemImpure(cart, item) {
  cart.items.push(item);
  cart.total += item.price;
  return cart;
}

// Pure function (no side effects)
function addItemPure(cart, item) {
  return {
    ...cart,
    items: [...cart.items, item],
    total: cart.total + item.price
  };
}

// Immutable array operations
const numbers = [1, 2, 3, 4, 5];

// Add to array
const withSix = [...numbers, 6];

// Remove from array
const withoutThree = numbers.filter(n => n !== 3);

// Update array element
const doubled = numbers.map(n => n === 3 ? n * 2 : n);

// Immutable object operations
const user = { name: 'John', age: 30 };

// Update property
const olderUser = { ...user, age: 31 };

// Add property
const withEmail = { ...user, email: 'john@example.com' };

// Remove property
const { age, ...withoutAge } = user;

// Deep cloning (simple approach)
const deepClone = obj => JSON.parse(JSON.stringify(obj));

// Better deep cloning
const structuredClone = obj => globalThis.structuredClone(obj);
```

## 현대적인 클래스 기능

```javascript
// Class syntax
class User {
  // Private fields
  #password;

  // Public fields
  id;
  name;

  // Static field
  static count = 0;

  constructor(id, name, password) {
    this.id = id;
    this.name = name;
    this.#password = password;
    User.count++;
  }

  // Public method
  greet() {
    return `Hello, ${this.name}`;
  }

  // Private method
  #hashPassword(password) {
    return `hashed_${password}`;
  }

  // Getter
  get displayName() {
    return this.name.toUpperCase();
  }

  // Setter
  set password(newPassword) {
    this.#password = this.#hashPassword(newPassword);
  }

  // Static method
  static create(id, name, password) {
    return new User(id, name, password);
  }
}

// Inheritance
class Admin extends User {
  constructor(id, name, password, role) {
    super(id, name, password);
    this.role = role;
  }

  greet() {
    return `${super.greet()}, I'm an admin`;
  }
}
```

## 모듈 (ES6)

```javascript
// Exporting
// math.js
export const PI = 3.14159;
export function add(a, b) {
  return a + b;
}
export class Calculator {
  // ...
}

// Default export
export default function multiply(a, b) {
  return a * b;
}

// Importing
// app.js
import multiply, { PI, add, Calculator } from './math.js';

// Rename imports
import { add as sum } from './math.js';

// Import all
import * as Math from './math.js';

// Dynamic imports
const module = await import('./math.js');
const { add } = await import('./math.js');

// Conditional loading
if (condition) {
  const module = await import('./feature.js');
  module.init();
}
```

## Iterators 및 Generators

```javascript
// Custom iterator
const range = {
  from: 1,
  to: 5,

  [Symbol.iterator]() {
    return {
      current: this.from,
      last: this.to,

      next() {
        if (this.current <= this.last) {
          return { done: false, value: this.current++ };
        } else {
          return { done: true };
        }
      }
    };
  }
};

for (const num of range) {
  console.log(num);  // 1, 2, 3, 4, 5
}

// Generator function
function* rangeGenerator(from, to) {
  for (let i = from; i <= to; i++) {
    yield i;
  }
}

for (const num of rangeGenerator(1, 5)) {
  console.log(num);
}

// Infinite generator
function* fibonacci() {
  let [prev, curr] = [0, 1];
  while (true) {
    yield curr;
    [prev, curr] = [curr, prev + curr];
  }
}

// Async generator
async function* fetchPages(url) {
  let page = 1;
  while (true) {
    const response = await fetch(`${url}?page=${page}`);
    const data = await response.json();
    if (data.length === 0) break;
    yield data;
    page++;
  }
}

for await (const page of fetchPages('/api/users')) {
  console.log(page);
}
```

## 현대적인 Operators

```javascript
// Optional chaining
const user = { name: 'John', address: { city: 'NYC' } };
const city = user?.address?.city;
const zipCode = user?.address?.zipCode;  // undefined

// Function call
const result = obj.method?.();

// Array access
const first = arr?.[0];

// Nullish coalescing
const value = null ?? 'default';      // 'default'
const value = undefined ?? 'default'; // 'default'
const value = 0 ?? 'default';         // 0 (not 'default')
const value = '' ?? 'default';        // '' (not 'default')

// Logical assignment
let a = null;
a ??= 'default';  // a = 'default'

let b = 5;
b ??= 10;  // b = 5 (unchanged)

let obj = { count: 0 };
obj.count ||= 1;  // obj.count = 1
obj.count &&= 2;  // obj.count = 2
```

## 성능 최적화

```javascript
// Debounce
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

const searchDebounced = debounce(search, 300);

// Throttle
function throttle(fn, limit) {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

const scrollThrottled = throttle(handleScroll, 100);

// Lazy evaluation
function* lazyMap(iterable, transform) {
  for (const item of iterable) {
    yield transform(item);
  }
}

// Use only what you need
const numbers = [1, 2, 3, 4, 5];
const doubled = lazyMap(numbers, x => x * 2);
const first = doubled.next().value;  // Only computes first value
```

## 최선의 관행

1. **Use const 에 의해 default**: 오직 use let 때 reassignment is 필요한
2. **Prefer arrow 함수**: 특히 위한 callbacks
3. **Use 템플릿 literals**: Instead of string concatenation
4. **Destructure 객체 및 배열**: 위한 cleaner 코드
5. **Use 비동기/await**: Instead of 프로미스 chains
6. **Avoid mutating 데이터**: Use 분산 운영자 및 배열 메서드
7. **Use 선택적 chaining**: Prevent "Cannot 읽은 속성 of undefined"
8. **Use nullish coalescing**: 위한 default 값
9. **Prefer 배열 메서드**: Over 전통적인 루프합니다
10. **Use 모듈**: 위한 더 나은 코드 조직
11. **Write pure 함수**: Easier 에 test 및 reason 약
12. **Use 의미 있는 가변 names**: Self-documenting 코드
13. **Keep 함수 small**: Single responsibility 원칙
14. **Handle 오류 적절하게**: Use try/catch 와 함께 비동기/await
15. **Use strict 최빈값**: `'use strict'` 위한 더 나은 오류 catching

## 일반적인 Pitfalls

1. **this 바인딩 confusion**: Use arrow 함수 또는 bind()
2. **비동기/await 없이 오류 처리**: 항상 use try/catch
3. **프로미스 생성 unnecessary**: Don't wrap 이미 비동기 함수
4. **Mutation of 객체**: Use 분산 운영자 또는 객체.assign()
5. **Forgetting await**: 비동기 함수 반환 promises
6. **차단 이벤트 루프**: Avoid synchronous 작업
7. **메모리 leaks**: Clean up 이벤트 listeners 및 timers
8. **Not 처리 프로미스 rejections**: Use catch() 또는 try/catch

## 리소스

- **MDN Web Docs**: https://developer.mozilla.org/en-US/docs/Web/JavaScript
- **JavaScript.info**: https://javascript.info/
- **You Don't Know JS**: https://github.com/getify/You-Dont-Know-JS
- **Eloquent JavaScript**: https://eloquentjavascript.net/
- **ES6 기능**: http://es6-features.org/
