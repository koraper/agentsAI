---
name: debugging-strategies
description: 마스터 systematic 디버깅 techniques, profiling tools, 및 근 cause 분석 에 efficiently track down 버그 전반에 걸쳐 어떤 codebase 또는 technology 스택. Use 때 investigating 버그, 성능 이슈, 또는 unexpected behavior.
---

# 디버깅 Strategies

Transform 디버깅 에서 frustrating guesswork into systematic 문제-solving 와 함께 입증된 strategies, 강력한 tools, 및 methodical approaches.

## 때 에 Use This Skill

- 추적 down elusive 버그
- Investigating 성능 이슈
- Understanding unfamiliar codebases
- 디버깅 production 이슈
- Analyzing crash dumps 및 스택 추적합니다
- Profiling 애플리케이션 성능
- Investigating 메모리 leaks
- 디버깅 분산 시스템

## 핵심 원칙

### 1. The Scientific 메서드

**1. Observe**: 무엇's the actual behavior?
**2. Hypothesize**: 무엇 could be causing it?
**3. Experiment**: Test your 가설
**4. Analyze**: Did it prove/disprove your 이론?
**5. Repeat**: 까지 you find the 근 cause

### 2. 디버깅 Mindset

**Don't Assume:**
- "It can't be X" - 예 it can
- "I didn't 변경 Y" - Check anyway
- "It 작동합니다 에 my machine" - Find out 왜

**do:**
- Reproduce consistently
- Isolate the 문제
- Keep 상세한 notes
- Question everything
- Take breaks 때 stuck

### 3. Rubber Duck 디버깅

Explain your 코드 및 문제 out loud (에 a rubber duck, colleague, 또는 yourself). 자주 reveals the 이슈.

## Systematic 디버깅 프로세스

### 단계 1: Reproduce

```markdown
## Reproduction Checklist

1. **Can you reproduce it?**
   - Always? Sometimes? Randomly?
   - Specific conditions needed?
   - Can others reproduce it?

2. **Create minimal reproduction**
   - Simplify to smallest example
   - Remove unrelated code
   - Isolate the problem

3. **Document steps**
   - Write down exact steps
   - Note environment details
   - Capture error messages
```

### 단계 2: Gather 정보

```markdown
## Information Collection

1. **Error Messages**
   - Full stack trace
   - Error codes
   - Console/log output

2. **Environment**
   - OS version
   - Language/runtime version
   - Dependencies versions
   - Environment variables

3. **Recent Changes**
   - Git history
   - Deployment timeline
   - Configuration changes

4. **Scope**
   - Affects all users or specific ones?
   - All browsers or specific ones?
   - Production only or also dev?
```

### 단계 3: 폼 가설

```markdown
## Hypothesis Formation

Based on gathered info, ask:

1. **What changed?**
   - Recent code changes
   - Dependency updates
   - Infrastructure changes

2. **What's different?**
   - Working vs broken environment
   - Working vs broken user
   - Before vs after

3. **Where could this fail?**
   - Input validation
   - Business logic
   - Data layer
   - External services
```

### 단계 4: Test & Verify

```markdown
## Testing Strategies

1. **Binary Search**
   - Comment out half the code
   - Narrow down problematic section
   - Repeat until found

2. **Add Logging**
   - Strategic console.log/print
   - Track variable values
   - Trace execution flow

3. **Isolate Components**
   - Test each piece separately
   - Mock dependencies
   - Remove complexity

4. **Compare Working vs Broken**
   - Diff configurations
   - Diff environments
   - Diff data
```

## 디버깅 Tools

### JavaScript/TypeScript 디버깅

```typescript
// Chrome DevTools Debugger
function processOrder(order: Order) {
    debugger;  // Execution pauses here

    const total = calculateTotal(order);
    console.log('Total:', total);

    // Conditional breakpoint
    if (order.items.length > 10) {
        debugger;  // Only breaks if condition true
    }

    return total;
}

// Console debugging techniques
console.log('Value:', value);                    // Basic
console.table(arrayOfObjects);                   // Table format
console.time('operation'); /* code */ console.timeEnd('operation');  // Timing
console.trace();                                 // Stack trace
console.assert(value > 0, 'Value must be positive');  // Assertion

// Performance profiling
performance.mark('start-operation');
// ... operation code
performance.mark('end-operation');
performance.measure('operation', 'start-operation', 'end-operation');
console.log(performance.getEntriesByType('measure'));
```

**VS 코드 디버거 구성:**
```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "node",
            "request": "launch",
            "name": "Debug Program",
            "program": "${workspaceFolder}/src/index.ts",
            "preLaunchTask": "tsc: build - tsconfig.json",
            "outFiles": ["${workspaceFolder}/dist/**/*.js"],
            "skipFiles": ["<node_internals>/**"]
        },
        {
            "type": "node",
            "request": "launch",
            "name": "Debug Tests",
            "program": "${workspaceFolder}/node_modules/jest/bin/jest",
            "args": ["--runInBand", "--no-cache"],
            "console": "integratedTerminal"
        }
    ]
}
```

### Python 디버깅

```python
# Built-in debugger (pdb)
import pdb

def calculate_total(items):
    total = 0
    pdb.set_trace()  # Debugger starts here

    for item in items:
        total += item.price * item.quantity

    return total

# Breakpoint (Python 3.7+)
def process_order(order):
    breakpoint()  # More convenient than pdb.set_trace()
    # ... code

# Post-mortem debugging
try:
    risky_operation()
except Exception:
    import pdb
    pdb.post_mortem()  # Debug at exception point

# IPython debugging (ipdb)
from ipdb import set_trace
set_trace()  # Better interface than pdb

# Logging for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def fetch_user(user_id):
    logger.debug(f'Fetching user: {user_id}')
    user = db.query(User).get(user_id)
    logger.debug(f'Found user: {user}')
    return user

# Profile performance
import cProfile
import pstats

cProfile.run('slow_function()', 'profile_stats')
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 slowest
```

### Go 디버깅

```go
// Delve debugger
// Install: go install github.com/go-delve/delve/cmd/dlv@latest
// Run: dlv debug main.go

import (
    "fmt"
    "runtime"
    "runtime/debug"
)

// Print stack trace
func debugStack() {
    debug.PrintStack()
}

// Panic recovery with debugging
func processRequest() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Panic:", r)
            debug.PrintStack()
        }
    }()

    // ... code that might panic
}

// Memory profiling
import _ "net/http/pprof"
// Visit http://localhost:6060/debug/pprof/

// CPU profiling
import (
    "os"
    "runtime/pprof"
)

f, _ := os.Create("cpu.prof")
pprof.StartCPUProfile(f)
defer pprof.StopCPUProfile()
// ... code to profile
```

## 고급 디버깅 Techniques

### 기법 1: 바이너리 Search 디버깅

```bash
# Git bisect for finding regression
git bisect start
git bisect bad                    # Current commit is bad
git bisect good v1.0.0            # v1.0.0 was good

# Git checks out middle commit
# Test it, then:
git bisect good   # if it works
git bisect bad    # if it's broken

# Continue until bug found
git bisect reset  # when done
```

### 기법 2: Differential 디버깅

Compare 작업 vs 고장난:

```markdown
## What's Different?

| Aspect       | Working         | Broken          |
|--------------|-----------------|-----------------|
| Environment  | Development     | Production      |
| Node version | 18.16.0         | 18.15.0         |
| Data         | Empty DB        | 1M records      |
| User         | Admin           | Regular user    |
| Browser      | Chrome          | Safari          |
| Time         | During day      | After midnight  |

Hypothesis: Time-based issue? Check timezone handling.
```

### 기법 3: Trace 디버깅

```typescript
// Function call tracing
function trace(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = function(...args: any[]) {
        console.log(`Calling ${propertyKey} with args:`, args);
        const result = originalMethod.apply(this, args);
        console.log(`${propertyKey} returned:`, result);
        return result;
    };

    return descriptor;
}

class OrderService {
    @trace
    calculateTotal(items: Item[]): number {
        return items.reduce((sum, item) => sum + item.price, 0);
    }
}
```

### 기법 4: 메모리 Leak 감지

```typescript
// Chrome DevTools Memory Profiler
// 1. Take heap snapshot
// 2. Perform action
// 3. Take another snapshot
// 4. Compare snapshots

// Node.js memory debugging
if (process.memoryUsage().heapUsed > 500 * 1024 * 1024) {
    console.warn('High memory usage:', process.memoryUsage());

    // Generate heap dump
    require('v8').writeHeapSnapshot();
}

// Find memory leaks in tests
let beforeMemory: number;

beforeEach(() => {
    beforeMemory = process.memoryUsage().heapUsed;
});

afterEach(() => {
    const afterMemory = process.memoryUsage().heapUsed;
    const diff = afterMemory - beforeMemory;

    if (diff > 10 * 1024 * 1024) {  // 10MB threshold
        console.warn(`Possible memory leak: ${diff / 1024 / 1024}MB`);
    }
});
```

## 디버깅 패턴 에 의해 이슈 유형

### 패턴 1: Intermittent 버그

```markdown
## Strategies for Flaky Bugs

1. **Add extensive logging**
   - Log timing information
   - Log all state transitions
   - Log external interactions

2. **Look for race conditions**
   - Concurrent access to shared state
   - Async operations completing out of order
   - Missing synchronization

3. **Check timing dependencies**
   - setTimeout/setInterval
   - Promise resolution order
   - Animation frame timing

4. **Stress test**
   - Run many times
   - Vary timing
   - Simulate load
```

### 패턴 2: 성능 이슈

```markdown
## Performance Debugging

1. **Profile first**
   - Don't optimize blindly
   - Measure before and after
   - Find bottlenecks

2. **Common culprits**
   - N+1 queries
   - Unnecessary re-renders
   - Large data processing
   - Synchronous I/O

3. **Tools**
   - Browser DevTools Performance tab
   - Lighthouse
   - Python: cProfile, line_profiler
   - Node: clinic.js, 0x
```

### 패턴 3: Production 버그

```markdown
## Production Debugging

1. **Gather evidence**
   - Error tracking (Sentry, Bugsnag)
   - Application logs
   - User reports
   - Metrics/monitoring

2. **Reproduce locally**
   - Use production data (anonymized)
   - Match environment
   - Follow exact steps

3. **Safe investigation**
   - Don't change production
   - Use feature flags
   - Add monitoring/logging
   - Test fixes in staging
```

## 최선의 관행

1. **Reproduce 첫 번째**: Can't fix 무엇 you can't reproduce
2. **Isolate the 문제**: Remove complexity 까지 최소 case
3. **읽은 오류 메시지**: They're 일반적으로 helpful
4. **Check 최근 변경합니다**: Most 버그 are 최근
5. **Use 버전 Control**: Git bisect, blame, history
6. **Take Breaks**: Fresh eyes see 더 나은
7. **Document Findings**: Help 미래 you
8. **Fix 근 Cause**: Not 방금 symptoms

## 일반적인 디버깅 Mistakes

- **Making 여러 변경합니다**: 변경 one thing 에서 a 시간
- **Not 읽는 오류 메시지**: 읽은 the 전체 스택 trace
- **Assuming It's 복잡한**: 자주 it's 간단한
- **Debug 로깅 에서 Prod**: Remove 이전 shipping
- **Not 사용하여 디버거**: console.log isn't 항상 최선의
- **Giving Up 또한 Soon**: 지속성 pays 꺼짐
- **Not 테스트 the Fix**: Verify it actually 작동합니다

## Quick 디버깅 Checklist

```markdown
## When Stuck, Check:

- [ ] Spelling errors (typos in variable names)
- [ ] Case sensitivity (fileName vs filename)
- [ ] Null/undefined values
- [ ] Array index off-by-one
- [ ] Async timing (race conditions)
- [ ] Scope issues (closure, hoisting)
- [ ] Type mismatches
- [ ] Missing dependencies
- [ ] Environment variables
- [ ] File paths (absolute vs relative)
- [ ] Cache issues (clear cache)
- [ ] Stale data (refresh database)
```

## 리소스

- **참조/디버깅-tools-가이드.md**: 포괄적인 tool 문서화
- **참조/성능-profiling.md**: 성능 디버깅 가이드
- **참조/production-디버깅.md**: 디버깅 live 시스템
- **자산/디버깅-checklist.md**: Quick 참조 checklist
- **자산/일반적인-버그.md**: 일반적인 버그 패턴
- **스크립트/debug-helper.ts**: 디버깅 utility 함수
