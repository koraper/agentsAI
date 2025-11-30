Execute a 포괄적인 Test-Driven Development (TDD) 워크플로우 와 함께 strict red-green-refactor discipline:

[Extended thinking: This 워크플로우 enforces test-first development 통해 coordinated agent 오케스트레이션. Each phase of the TDD cycle is strictly enforced 와 함께 fail-first verification, incremental 구현, 및 continuous refactoring. The 워크플로우 supports both single test 및 test suite approaches 와 함께 configurable coverage thresholds.]

## 구성

### Coverage Thresholds
- Minimum line coverage: 80%
- Minimum branch coverage: 75%
- 중요한 path coverage: 100%

### Refactoring Triggers
- Cyclomatic complexity > 10
- Method length > 20 lines
- Class length > 200 lines
- Duplicate code blocks > 3 lines

## Phase 1: Test Specification 및 설계

### 1. Requirements Analysis
- Use Task tool 와 함께 subagent_type="포괄적인-review::아키텍트-review"
- Prompt: "Analyze requirements 위한: $ARGUMENTS. Define acceptance criteria, identify edge cases, 및 create test scenarios. Output a 포괄적인 test specification."
- Output: Test specification, acceptance criteria, edge case matrix
- Validation: Ensure all requirements have corresponding test scenarios

### 2. Test 아키텍처 설계
- Use Task tool 와 함께 subagent_type="unit-테스트::test-automator"
- Prompt: "설계 test 아키텍처 위한: $ARGUMENTS based 에 test specification. Define test structure, fixtures, mocks, 및 test data strategy. Ensure testability 및 maintainability."
- Output: Test 아키텍처, fixture 설계, mock strategy
- Validation: 아키텍처 supports isolated, fast, 신뢰할 수 있는 테스트합니다

## Phase 2: RED - Write Failing 테스트합니다

### 3. Write Unit 테스트합니다 (Failing)
- Use Task tool 와 함께 subagent_type="unit-테스트::test-automator"
- Prompt: "Write FAILING unit 테스트합니다 위한: $ARGUMENTS. 테스트합니다 must fail initially. Include edge cases, error scenarios, 및 happy paths. DO NOT implement production code."
- Output: Failing unit 테스트합니다, test 문서화
- **중요한**: Verify all 테스트합니다 fail 와 함께 expected error messages

### 4. Verify Test Failure
- Use Task tool 와 함께 subagent_type="tdd-workflows::code-검토자"
- Prompt: "Verify that all 테스트합니다 위한: $ARGUMENTS are failing correctly. Ensure failures are 위한 the right reasons (missing 구현, not test errors). Confirm no false positives."
- Output: Test failure verification report
- **GATE**: Do not proceed until all 테스트합니다 fail appropriately

## Phase 3: GREEN - Make 테스트합니다 Pass

### 5. Minimal 구현
- Use Task tool 와 함께 subagent_type="backend-development::backend-아키텍트"
- Prompt: "Implement MINIMAL code 에 make 테스트합니다 pass 위한: $ARGUMENTS. Focus only 에 making 테스트합니다 green. Do not add extra features 또는 optimizations. Keep it 간단한."
- Output: Minimal working 구현
- Constraint: No code beyond what's needed 에 pass 테스트합니다

### 6. Verify Test Success
- Use Task tool 와 함께 subagent_type="unit-테스트::test-automator"
- Prompt: "Run all 테스트합니다 위한: $ARGUMENTS 및 verify they pass. Check test coverage metrics. Ensure no 테스트합니다 were accidentally broken."
- Output: Test execution report, coverage metrics
- **GATE**: All 테스트합니다 must pass 이전 proceeding

## Phase 4: REFACTOR - Improve 코드 품질

### 7. Code Refactoring
- Use Task tool 와 함께 subagent_type="tdd-workflows::code-검토자"
- Prompt: "Refactor 구현 위한: $ARGUMENTS 동안 keeping 테스트합니다 green. Apply SOLID principles, remove duplication, improve naming, 및 optimize 성능. Run 테스트합니다 이후 each refactoring."
- Output: Refactored code, refactoring report
- Constraint: 테스트합니다 must remain green throughout

### 8. Test Refactoring
- Use Task tool 와 함께 subagent_type="unit-테스트::test-automator"
- Prompt: "Refactor 테스트합니다 위한: $ARGUMENTS. Remove test duplication, improve test names, extract common fixtures, 및 enhance test readability. Ensure 테스트합니다 still provide same coverage."
- Output: Refactored 테스트합니다, improved test structure
- Validation: Coverage metrics unchanged 또는 improved

## Phase 5: 통합 및 System 테스트합니다

### 9. Write 통합 테스트합니다 (Failing First)
- Use Task tool 와 함께 subagent_type="unit-테스트::test-automator"
- Prompt: "Write FAILING 통합 테스트합니다 위한: $ARGUMENTS. Test component interactions, API contracts, 및 data flow. 테스트합니다 must fail initially."
- Output: Failing 통합 테스트합니다
- Validation: 테스트합니다 fail due 에 missing 통합 logic

### 10. Implement 통합
- Use Task tool 와 함께 subagent_type="backend-development::backend-아키텍트"
- Prompt: "Implement 통합 code 위한: $ARGUMENTS 에 make 통합 테스트합니다 pass. Focus 에 component interaction 및 data flow."
- Output: 통합 구현
- Validation: All 통합 테스트합니다 pass

## Phase 6: Continuous Improvement Cycle

### 11. 성능 및 Edge Case 테스트합니다
- Use Task tool 와 함께 subagent_type="unit-테스트::test-automator"
- Prompt: "Add 성능 테스트합니다 및 additional edge case 테스트합니다 위한: $ARGUMENTS. Include stress 테스트합니다, boundary 테스트합니다, 및 error recovery 테스트합니다."
- Output: Extended test suite
- Metric: Increased test coverage 및 scenario coverage

### 12. Final 코드 리뷰
- Use Task tool 와 함께 subagent_type="포괄적인-review::아키텍트-review"
- Prompt: "Perform 포괄적인 review of: $ARGUMENTS. Verify TDD process was followed, check 코드 품질, test quality, 및 coverage. Suggest improvements."
- Output: Review report, improvement suggestions
- Action: Implement 중요한 suggestions 동안 maintaining green 테스트합니다

## Incremental Development Mode

위한 test-에 의해-test development:
1. Write ONE failing test
2. Make ONLY that test pass
3. Refactor 필요한 경우
4. Repeat 위한 next test

Use this approach 에 의해 adding `--incremental` flag 에 focus 에 one test 에서 a time.

## Test Suite Mode

위한 포괄적인 test suite development:
1. Write ALL 테스트합니다 위한 a feature/module (failing)
2. Implement code 에 pass ALL 테스트합니다
3. Refactor entire module
4. Add 통합 테스트합니다

Use this approach 에 의해 adding `--suite` flag 위한 batch test development.

## Validation Checkpoints

### RED Phase Validation
- [ ] All 테스트합니다 written 이전 구현
- [ ] All 테스트합니다 fail 와 함께 meaningful error messages
- [ ] Test failures are due 에 missing 구현
- [ ] No test passes accidentally

### GREEN Phase Validation
- [ ] All 테스트합니다 pass
- [ ] No extra code beyond test requirements
- [ ] Coverage meets minimum thresholds
- [ ] No test was modified 에 make it pass

### REFACTOR Phase Validation
- [ ] All 테스트합니다 still pass 이후 refactoring
- [ ] Code complexity reduced
- [ ] Duplication eliminated
- [ ] 성능 improved 또는 maintained
- [ ] Test readability improved

## Coverage Reports

Generate coverage reports 이후 each phase:
- Line coverage
- Branch coverage
- Function coverage
- Statement coverage

## Failure Recovery

If TDD discipline is broken:
1. **STOP** immediately
2. Identify which phase was violated
3. Rollback 에 last valid state
4. Resume 에서 correct phase
5. Document lesson learned

## TDD Metrics Tracking

Track 및 report:
- Time 에서 each phase (Red/Green/Refactor)
- Number of test-구현 cycles
- Coverage progression
- Refactoring frequency
- Defect escape rate

## Anti-Patterns 에 Avoid

- Writing 구현 이전 테스트합니다
- Writing 테스트합니다 that already pass
- Skipping the refactor phase
- Writing multiple features 없이 테스트합니다
- Modifying 테스트합니다 에 make them pass
- Ignoring failing 테스트합니다
- Writing 테스트합니다 이후 구현

## Success Criteria

- 100% of code written test-first
- All 테스트합니다 pass continuously
- Coverage exceeds thresholds
- Code complexity within limits
- Zero defects 에서 covered code
- Clear test 문서화
- Fast test execution (< 5 seconds 위한 unit 테스트합니다)

## Notes

- Enforce strict RED-GREEN-REFACTOR discipline
- Each phase must be completed 이전 moving 에 next
- 테스트합니다 are the specification
- If a test is hard 에 write, the 설계 needs improvement
- Refactoring is NOT optional
- Keep test execution fast
- 테스트합니다 should be independent 및 isolated

TDD 구현 위한: $ARGUMENTS