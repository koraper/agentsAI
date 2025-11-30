Refactor code 와 함께 confidence 사용하여 포괄적인 test safety net:

[Extended thinking: This tool uses the tdd-orchestrator agent (opus model) 위한 sophisticated refactoring 동안 maintaining all 테스트합니다 green. It applies 설계 patterns, improves 코드 품질, 및 최적화합니다 성능 와 함께 the safety of 포괄적인 test coverage.]

## Usage

Use Task tool 와 함께 subagent_type="tdd-orchestrator" 에 perform safe refactoring.

Prompt: "Refactor this code 동안 keeping all 테스트합니다 green: $ARGUMENTS. Apply TDD refactor phase:

## Core Process

**1. Pre-Assessment**
- Run 테스트합니다 에 establish green baseline
- Analyze code smells 및 test coverage
- Document current 성능 metrics
- Create incremental refactoring plan

**2. Code Smell Detection**
- Duplicated code → Extract methods/classes
- Long methods → Decompose into focused functions
- Large classes → Split responsibilities
- Long parameter lists → Parameter objects
- Feature Envy → Move methods 에 appropriate classes
- Primitive Obsession → Value objects
- Switch statements → Polymorphism
- Dead code → Remove

**3. 설계 Patterns**
- Apply Creational (Factory, Builder, Singleton)
- Apply Structural (Adapter, Facade, Decorator)
- Apply Behavioral (Strategy, Observer, Command)
- Apply Domain (Repository, Service, Value Objects)
- Use patterns only where they add clear value

**4. SOLID Principles**
- Single Responsibility: One reason 에 change
- Open/Closed: Open 위한 extension, closed 위한 modification
- Liskov Substitution: Subtypes substitutable
- Interface Segregation: Small, focused interfaces
- Dependency Inversion: Depend 에 abstractions

**5. Refactoring Techniques**
- Extract Method/Variable/Interface
- Inline unnecessary indirection
- Rename 위한 clarity
- Move Method/Field 에 appropriate classes
- Replace Magic Numbers 와 함께 constants
- Encapsulate fields
- Replace Conditional 와 함께 Polymorphism
- Introduce Null Object

**6. 성능 최적화**
- Profile 에 identify bottlenecks
- Optimize algorithms 및 data structures
- Implement caching where beneficial
- Reduce database queries (N+1 elimination)
- Lazy loading 및 pagination
- Always measure 이전 및 이후

**7. Incremental Steps**
- Make small, atomic changes
- Run 테스트합니다 이후 each modification
- Commit 이후 each successful refactoring
- Keep refactoring separate 에서 behavior changes
- Use scaffolding 필요할 때

**8. 아키텍처 Evolution**
- Layer separation 및 dependency management
- Module boundaries 및 interface definition
- Event-driven patterns 위한 decoupling
- Database access 패턴 최적화

**9. Safety Verification**
- Run full test suite 이후 each change
- 성능 regression 테스트
- Mutation 테스트 위한 test effectiveness
- Rollback plan 위한 major changes

**10. 고급 Patterns**
- Strangler Fig: Gradual legacy replacement
- Branch 에 의해 Abstraction: Large-scale changes
- Parallel Change: Expand-contract 패턴
- Mikado Method: Dependency graph navigation

## Output Requirements

- Refactored code 와 함께 improvements applied
- Test results (all green)
- 이전/이후 metrics comparison
- Applied refactoring techniques list
- 성능 improvement measurements
- Remaining 기술 부채 assessment

## Safety Checklist

이전 committing:
- ✓ All 테스트합니다 pass (100% green)
- ✓ No functionality regression
- ✓ 성능 metrics acceptable
- ✓ Code coverage maintained/improved
- ✓ 문서화 updated

## Recovery Protocol

If 테스트합니다 fail:
- Immediately revert last change
- Identify breaking refactoring
- Apply smaller incremental changes
- Use 버전 관리 위한 safe experimentation

## Example: Extract Method 패턴

**이전:**
```typescript
class OrderProcessor {
  processOrder(order: Order): ProcessResult {
    // Validation
    if (!order.customerId || order.items.length === 0) {
      return { success: false, error: "Invalid order" };
    }

    // Calculate totals
    let subtotal = 0;
    for (const item of order.items) {
      subtotal += item.price * item.quantity;
    }
    let total = subtotal + (subtotal * 0.08) + (subtotal > 100 ? 0 : 15);

    // Process payment...
    // Update inventory...
    // Send confirmation...
  }
}
```

**이후:**
```typescript
class OrderProcessor {
  async processOrder(order: Order): Promise<ProcessResult> {
    const validation = this.validateOrder(order);
    if (!validation.isValid) return ProcessResult.failure(validation.error);

    const orderTotal = OrderTotal.calculate(order);
    const inventoryCheck = await this.inventoryService.checkAvailability(order.items);
    if (!inventoryCheck.available) return ProcessResult.failure(inventoryCheck.reason);

    await this.paymentService.processPayment(order.paymentMethod, orderTotal.total);
    await this.inventoryService.reserveItems(order.items);
    await this.notificationService.sendOrderConfirmation(order, orderTotal);

    return ProcessResult.success(order.id, orderTotal.total);
  }

  private validateOrder(order: Order): ValidationResult {
    if (!order.customerId) return ValidationResult.invalid("Customer ID required");
    if (order.items.length === 0) return ValidationResult.invalid("Order must contain items");
    return ValidationResult.valid();
  }
}
```

**Applied:** Extract Method, Value Objects, Dependency Injection, Async patterns

Code 에 refactor: $ARGUMENTS"
