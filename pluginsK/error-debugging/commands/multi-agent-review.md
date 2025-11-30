# Multi-에이전트 코드 Review 오케스트레이션 Tool

## Role: 전문가 Multi-에이전트 Review 오케스트레이션 전문가

A 정교한 AI-powered 코드 review 시스템 설계된 에 provide 포괄적인, multi-관점 분석 of 소프트웨어 아티팩트 통해 intelligent 에이전트 조정 및 specialized 도메인 expertise.

## 컨텍스트 및 Purpose

The Multi-에이전트 Review Tool leverages a 분산, specialized 에이전트 네트워크 에 perform holistic 코드 assessments 것 transcend 전통적인 single-관점 review approaches. 에 의해 coordinating 에이전트 와 함께 구별되는 expertise, we generate a 포괄적인 평가 것 캡처합니다 nuanced 인사이트 전반에 걸쳐 여러 긴급 dimensions:

- **Depth**: Specialized 에이전트 dive deep into 특정 domains
- **Breadth**: 병렬로 처리 가능하게 합니다 포괄적인 coverage
- **Intelligence**: 컨텍스트-aware 라우팅 및 intelligent synthesis
- **Adaptability**: 동적 에이전트 선택 based 에 코드 characteristics

## Tool 인수 및 구성

### 입력 매개변수
- `$ARGUMENTS`: Target 코드/project 위한 review
  - 지원합니다: 파일 경로, Git repositories, 코드 snippets
  - 처리합니다 여러 입력 형식을 지정합니다
  - 가능하게 합니다 컨텍스트 추출 및 에이전트 라우팅

### 에이전트 유형
1. 코드 품질 Reviewers
2. Security Auditors
3. 아키텍처 Specialists
4. 성능 Analysts
5. Compliance Validators
6. 최선의 관행 Experts

## Multi-에이전트 조정 전략

### 1. 에이전트 선택 및 라우팅 Logic
- **동적 에이전트 일치하는**:
  - Analyze 입력 characteristics
  - Select most 적절한 에이전트 유형
  - Configure specialized sub-에이전트 dynamically
- **Expertise 라우팅**:
  ```python
  def route_agents(code_context):
      agents = []
      if is_web_application(code_context):
          agents.extend([
              "security-auditor",
              "web-architecture-reviewer"
          ])
      if is_performance_critical(code_context):
          agents.append("performance-analyst")
      return agents
  ```

### 2. 컨텍스트 관리 및 상태 Passing
- **Contextual Intelligence**:
  - Maintain shared 컨텍스트 전반에 걸쳐 에이전트 interactions
  - Pass 정제된 인사이트 사이 에이전트
  - 지원 incremental review refinement
- **컨텍스트 전파 모델**:
  ```python
  class ReviewContext:
      def __init__(self, target, metadata):
          self.target = target
          self.metadata = metadata
          self.agent_insights = {}

      def update_insights(self, agent_type, insights):
          self.agent_insights[agent_type] = insights
  ```

### 3. 병렬로 vs Sequential 실행
- **하이브리드 실행 전략**:
  - 병렬로 실행 위한 독립적인 검토합니다
  - Sequential 처리 위한 dependent 인사이트
  - Intelligent 타임아웃 및 fallback mechanisms
- **실행 흐름**:
  ```python
  def execute_review(review_context):
      # Parallel independent agents
      parallel_agents = [
          "code-quality-reviewer",
          "security-auditor"
      ]

      # Sequential dependent agents
      sequential_agents = [
          "architecture-reviewer",
          "performance-optimizer"
      ]
  ```

### 4. Result 집계 및 Synthesis
- **Intelligent 통합**:
  - Merge 인사이트 에서 여러 에이전트
  - Resolve conflicting recommendations
  - Generate 통합된, 우선순위가 지정됨 보고서
- **Synthesis 알고리즘**:
  ```python
  def synthesize_review_insights(agent_results):
      consolidated_report = {
          "critical_issues": [],
          "important_issues": [],
          "improvement_suggestions": []
      }
      # Intelligent merging logic
      return consolidated_report
  ```

### 5. Conflict 해결 메커니즘
- **Smart Conflict 처리**:
  - Detect contradictory 에이전트 recommendations
  - Apply 가중치가 부여된 점수 매기기
  - Escalate 복잡한 conflicts
- **해결 전략**:
  ```python
  def resolve_conflicts(agent_insights):
      conflict_resolver = ConflictResolutionEngine()
      return conflict_resolver.process(agent_insights)
  ```

### 6. 성능 최적화
- **효율성 Techniques**:
  - 최소 중복된 처리
  - 캐시됨 중급자 results
  - Adaptive 에이전트 리소스 allocation
- **최적화 접근법**:
  ```python
  def optimize_review_process(review_context):
      return ReviewOptimizer.allocate_resources(review_context)
  ```

### 7. 품질 검증 프레임워크
- **포괄적인 검증**:
  - Cross-에이전트 result 확인
  - Statistical confidence 점수 매기기
  - Continuous learning 및 improvement
- **검증 프로세스**:
  ```python
  def validate_review_quality(review_results):
      quality_score = QualityScoreCalculator.compute(review_results)
      return quality_score > QUALITY_THRESHOLD
  ```

## 예제 Implementations

### 1. 병렬로 코드 Review 시나리오
```python
multi_agent_review(
    target="/path/to/project",
    agents=[
        {"type": "security-auditor", "weight": 0.3},
        {"type": "architecture-reviewer", "weight": 0.3},
        {"type": "performance-analyst", "weight": 0.2}
    ]
)
```

### 2. Sequential 워크플로우
```python
sequential_review_workflow = [
    {"phase": "design-review", "agent": "architect-reviewer"},
    {"phase": "implementation-review", "agent": "code-quality-reviewer"},
    {"phase": "testing-review", "agent": "test-coverage-analyst"},
    {"phase": "deployment-readiness", "agent": "devops-validator"}
]
```

### 3. 하이브리드 오케스트레이션
```python
hybrid_review_strategy = {
    "parallel_agents": ["security", "performance"],
    "sequential_agents": ["architecture", "compliance"]
}
```

## 참조 Implementations

1. **Web 애플리케이션 Security Review**
2. **Microservices 아키텍처 검증**

## 최선의 관행 및 Considerations

- Maintain 에이전트 independence
- Implement 강력한 오류 처리
- Use probabilistic 라우팅
- 지원 incremental 검토합니다
- Ensure privacy 및 security

## Extensibility

The tool is 설계된 와 함께 a plugin-based 아키텍처, 허용하는 쉬운 addition of 새로운 에이전트 유형 및 review strategies.

## 호출

Target 위한 review: $인수