---
name: react-modernization
description: 업그레이드 React 애플리케이션 에 최신 버전, migrate 에서 클래스 컴포넌트 에 hooks, 및 adopt concurrent 기능. Use 때 modernizing React codebases, migrating 에 React Hooks, 또는 upgrading 에 최신 React 버전.
---

# React Modernization

마스터 React 버전 업그레이드합니다, 클래스 에 hooks 마이그레이션, concurrent 기능 adoption, 및 codemods 위한 자동화된 변환.

## 때 에 Use This Skill

- Upgrading React 애플리케이션 에 최신 버전
- Migrating 클래스 컴포넌트 에 기능적인 컴포넌트 와 함께 hooks
- Adopting concurrent React 기능 (Suspense, transitions)
- Applying codemods 위한 자동화된 리팩토링
- Modernizing 상태 관리 패턴
- Updating 에 TypeScript
- Improving 성능 와 함께 React 18+ 기능

## 버전 업그레이드 경로

### React 16 → 17 → 18

**Breaking 변경합니다 에 의해 버전:**

**React 17:**
- 이벤트 delegation 변경합니다
- 아니요 이벤트 풀링
- Effect cleanup timing
- JSX transform (아니요 React import 필요한)

**React 18:**
- Automatic 배치
- Concurrent 렌더링
- Strict 최빈값 변경합니다 (double 호출)
- 새로운 근 API
- Suspense 에 서버

## 클래스 에 Hooks 마이그레이션

### 상태 관리
```javascript
// Before: Class component
class Counter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      count: 0,
      name: ''
    };
  }

  increment = () => {
    this.setState({ count: this.state.count + 1 });
  }

  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button onClick={this.increment}>Increment</button>
      </div>
    );
  }
}

// After: Functional component with hooks
function Counter() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  const increment = () => {
    setCount(count + 1);
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
    </div>
  );
}
```

### Lifecycle 메서드 에 Hooks
```javascript
// Before: Lifecycle methods
class DataFetcher extends React.Component {
  state = { data: null, loading: true };

  componentDidMount() {
    this.fetchData();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.id !== this.props.id) {
      this.fetchData();
    }
  }

  componentWillUnmount() {
    this.cancelRequest();
  }

  fetchData = async () => {
    const data = await fetch(`/api/${this.props.id}`);
    this.setState({ data, loading: false });
  };

  cancelRequest = () => {
    // Cleanup
  };

  render() {
    if (this.state.loading) return <div>Loading...</div>;
    return <div>{this.state.data}</div>;
  }
}

// After: useEffect hook
function DataFetcher({ id }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    const fetchData = async () => {
      try {
        const response = await fetch(`/api/${id}`);
        const result = await response.json();

        if (!cancelled) {
          setData(result);
          setLoading(false);
        }
      } catch (error) {
        if (!cancelled) {
          console.error(error);
        }
      }
    };

    fetchData();

    // Cleanup function
    return () => {
      cancelled = true;
    };
  }, [id]); // Re-run when id changes

  if (loading) return <div>Loading...</div>;
  return <div>{data}</div>;
}
```

### 컨텍스트 및 HOCs 에 Hooks
```javascript
// Before: Context consumer and HOC
const ThemeContext = React.createContext();

class ThemedButton extends React.Component {
  static contextType = ThemeContext;

  render() {
    return (
      <button style={{ background: this.context.theme }}>
        {this.props.children}
      </button>
    );
  }
}

// After: useContext hook
function ThemedButton({ children }) {
  const { theme } = useContext(ThemeContext);

  return (
    <button style={{ background: theme }}>
      {children}
    </button>
  );
}

// Before: HOC for data fetching
function withUser(Component) {
  return class extends React.Component {
    state = { user: null };

    componentDidMount() {
      fetchUser().then(user => this.setState({ user }));
    }

    render() {
      return <Component {...this.props} user={this.state.user} />;
    }
  };
}

// After: Custom hook
function useUser() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser().then(setUser);
  }, []);

  return user;
}

function UserProfile() {
  const user = useUser();
  if (!user) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

## React 18 Concurrent 기능

### 새로운 근 API
```javascript
// Before: React 17
import ReactDOM from 'react-dom';

ReactDOM.render(<App />, document.getElementById('root'));

// After: React 18
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
root.render(<App />);
```

### Automatic 배치
```javascript
// React 18: All updates are batched
function handleClick() {
  setCount(c => c + 1);
  setFlag(f => !f);
  // Only one re-render (batched)
}

// Even in async:
setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
  // Still batched in React 18!
}, 1000);

// Opt out if needed
import { flushSync } from 'react-dom';

flushSync(() => {
  setCount(c => c + 1);
});
// Re-render happens here
setFlag(f => !f);
// Another re-render
```

### Transitions
```javascript
import { useState, useTransition } from 'react';

function SearchResults() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    // Urgent: Update input immediately
    setQuery(e.target.value);

    // Non-urgent: Update results (can be interrupted)
    startTransition(() => {
      setResults(searchResults(e.target.value));
    });
  };

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <Results data={results} />
    </>
  );
}
```

### Suspense 위한 데이터 가져오는
```javascript
import { Suspense } from 'react';

// Resource-based data fetching (with React 18)
const resource = fetchProfileData();

function ProfilePage() {
  return (
    <Suspense fallback={<Loading />}>
      <ProfileDetails />
      <Suspense fallback={<Loading />}>
        <ProfileTimeline />
      </Suspense>
    </Suspense>
  );
}

function ProfileDetails() {
  // This will suspend if data not ready
  const user = resource.user.read();
  return <h1>{user.name}</h1>;
}

function ProfileTimeline() {
  const posts = resource.posts.read();
  return <Timeline posts={posts} />;
}
```

## Codemods 위한 자동화

### Run React Codemods
```bash
# Install jscodeshift
npm install -g jscodeshift

# React 16.9 codemod (rename unsafe lifecycle methods)
npx react-codeshift <transform> <path>

# Example: Rename UNSAFE_ methods
npx react-codeshift --parser=tsx \
  --transform=react-codeshift/transforms/rename-unsafe-lifecycles.js \
  src/

# Update to new JSX Transform (React 17+)
npx react-codeshift --parser=tsx \
  --transform=react-codeshift/transforms/new-jsx-transform.js \
  src/

# Class to Hooks (third-party)
npx codemod react/hooks/convert-class-to-function src/
```

### 사용자 정의 Codemod 예제
```javascript
// custom-codemod.js
module.exports = function(file, api) {
  const j = api.jscodeshift;
  const root = j(file.source);

  // Find setState calls
  root.find(j.CallExpression, {
    callee: {
      type: 'MemberExpression',
      property: { name: 'setState' }
    }
  }).forEach(path => {
    // Transform to useState
    // ... transformation logic
  });

  return root.toSource();
};

// Run: jscodeshift -t custom-codemod.js src/
```

## 성능 최적화

### useMemo 및 useCallback
```javascript
function ExpensiveComponent({ items, filter }) {
  // Memoize expensive calculation
  const filteredItems = useMemo(() => {
    return items.filter(item => item.category === filter);
  }, [items, filter]);

  // Memoize callback to prevent child re-renders
  const handleClick = useCallback((id) => {
    console.log('Clicked:', id);
  }, []); // No dependencies, never changes

  return (
    <List items={filteredItems} onClick={handleClick} />
  );
}

// Child component with memo
const List = React.memo(({ items, onClick }) => {
  return items.map(item => (
    <Item key={item.id} item={item} onClick={onClick} />
  ));
});
```

### 코드 분할하는
```javascript
import { lazy, Suspense } from 'react';

// Lazy load components
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

## TypeScript 마이그레이션

```typescript
// Before: JavaScript
function Button({ onClick, children }) {
  return <button onClick={onClick}>{children}</button>;
}

// After: TypeScript
interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
}

function Button({ onClick, children }: ButtonProps) {
  return <button onClick={onClick}>{children}</button>;
}

// Generic components
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <>{items.map(renderItem)}</>;
}
```

## 마이그레이션 Checklist

```markdown
### Pre-Migration
- [ ] Update dependencies incrementally (not all at once)
- [ ] Review breaking changes in release notes
- [ ] Set up testing suite
- [ ] Create feature branch

### Class → Hooks Migration
- [ ] Identify class components to migrate
- [ ] Start with leaf components (no children)
- [ ] Convert state to useState
- [ ] Convert lifecycle to useEffect
- [ ] Convert context to useContext
- [ ] Extract custom hooks
- [ ] Test thoroughly

### React 18 Upgrade
- [ ] Update to React 17 first (if needed)
- [ ] Update react and react-dom to 18
- [ ] Update @types/react if using TypeScript
- [ ] Change to createRoot API
- [ ] Test with StrictMode (double invocation)
- [ ] Address concurrent rendering issues
- [ ] Adopt Suspense/Transitions where beneficial

### Performance
- [ ] Identify performance bottlenecks
- [ ] Add React.memo where appropriate
- [ ] Use useMemo/useCallback for expensive operations
- [ ] Implement code splitting
- [ ] Optimize re-renders

### Testing
- [ ] Update test utilities (React Testing Library)
- [ ] Test with React 18 features
- [ ] Check for warnings in console
- [ ] Performance testing
```

## 리소스

- **참조/breaking-변경합니다.md**: 버전-특정 breaking 변경합니다
- **참조/codemods.md**: Codemod usage 가이드
- **참조/hooks-마이그레이션.md**: 포괄적인 hooks 패턴
- **참조/concurrent-기능.md**: React 18 concurrent 기능
- **자산/codemod-config.json**: Codemod configurations
- **자산/마이그레이션-checklist.md**: 단계-에 의해-단계 checklist
- **스크립트/apply-codemods.sh**: 자동화된 codemod 스크립트

## 최선의 관행

1. **Incremental 마이그레이션**: Don't migrate everything 에서 once
2. **Test 철저히**: 포괄적인 테스트 에서 각 단계
3. **Use Codemods**: Automate repetitive transformations
4. **Start 간단한**: Begin 와 함께 leaf 컴포넌트
5. **Leverage StrictMode**: catch 이슈 early
6. **모니터 성능**: 측정 이전 및 이후
7. **Document 변경합니다**: Keep 마이그레이션 log

## 일반적인 Pitfalls

- Forgetting useEffect 종속성
- Over-사용하여 useMemo/useCallback
- Not 처리 cleanup 에서 useEffect
- Mixing 클래스 및 기능적인 패턴
- Ignoring StrictMode 경고
- Breaking 변경 가정
