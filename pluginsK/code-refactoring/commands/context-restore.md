# 컨텍스트 복원: 고급 Semantic 메모리 Rehydration

## Role 문

전문가 컨텍스트 복원 전문가 focused 에 intelligent, semantic-aware 컨텍스트 검색 및 reconstruction 전반에 걸쳐 복잡한 multi-에이전트 AI 워크플로우. Specializes 에서 preserving 및 reconstructing project 지식 와 함께 high fidelity 및 최소 정보 loss.

## 컨텍스트 Overview

The 컨텍스트 복원 tool is a 정교한 메모리 관리 시스템 설계된 에:
- Recover 및 reconstruct project 컨텍스트 전반에 걸쳐 분산 AI 워크플로우
- Enable seamless continuity 에서 복잡한, long-실행 중 projects
- Provide intelligent, semantically-aware 컨텍스트 rehydration
- Maintain historical 지식 무결성 및 결정 traceability

## 핵심 요구사항 및 인수

### 입력 매개변수
- `context_source`: Primary 컨텍스트 스토리지 위치 (vector 데이터베이스, 파일 시스템)
- `project_identifier`: 고유한 project namespace
- `restoration_mode`:
  - `full`: 완전한 컨텍스트 복원
  - `incremental`: 부분 컨텍스트 업데이트
  - `diff`: Compare 및 merge 컨텍스트 버전
- `token_budget`: Maximum 컨텍스트 토큰 에 restore (default: 8192)
- `relevance_threshold`: Semantic similarity cutoff 위한 컨텍스트 컴포넌트 (default: 0.75)

## 고급 컨텍스트 검색 Strategies

### 1. Semantic Vector Search
- Utilize multi-dimensional embedding 모델 위한 컨텍스트 검색
- Employ cosine similarity 및 vector 클러스터링 techniques
- 지원 multi-modal embedding (text, 코드, architectural 다이어그램)

```python
def semantic_context_retrieve(project_id, query_vector, top_k=5):
    """Semantically retrieve most relevant context vectors"""
    vector_db = VectorDatabase(project_id)
    matching_contexts = vector_db.search(
        query_vector,
        similarity_threshold=0.75,
        max_results=top_k
    )
    return rank_and_filter_contexts(matching_contexts)
```

### 2. Relevance 필터링 및 순위
- Implement multi-단계 relevance 점수 매기기
- Consider temporal decay, semantic similarity, 및 historical impact
- 동적 가중치 부여 of 컨텍스트 컴포넌트

```python
def rank_context_components(contexts, current_state):
    """Rank context components based on multiple relevance signals"""
    ranked_contexts = []
    for context in contexts:
        relevance_score = calculate_composite_score(
            semantic_similarity=context.semantic_score,
            temporal_relevance=context.age_factor,
            historical_impact=context.decision_weight
        )
        ranked_contexts.append((context, relevance_score))

    return sorted(ranked_contexts, key=lambda x: x[1], reverse=True)
```

### 3. 컨텍스트 Rehydration 패턴
- Implement incremental 컨텍스트 로드
- 지원 부분 및 전체 컨텍스트 reconstruction
- Manage 토큰 budgets dynamically

```python
def rehydrate_context(project_context, token_budget=8192):
    """Intelligent context rehydration with token budget management"""
    context_components = [
        'project_overview',
        'architectural_decisions',
        'technology_stack',
        'recent_agent_work',
        'known_issues'
    ]

    prioritized_components = prioritize_components(context_components)
    restored_context = {}

    current_tokens = 0
    for component in prioritized_components:
        component_tokens = estimate_tokens(component)
        if current_tokens + component_tokens <= token_budget:
            restored_context[component] = load_component(component)
            current_tokens += component_tokens

    return restored_context
```

### 4. 세션 상태 Reconstruction
- Reconstruct 에이전트 워크플로우 상태
- Preserve 결정 trails 및 reasoning contexts
- 지원 multi-에이전트 collaboration history

### 5. 컨텍스트 병합하는 및 Conflict 해결
- Implement three-way merge strategies
- Detect 및 resolve semantic conflicts
- Maintain provenance 및 결정 traceability

### 6. Incremental 컨텍스트 로드
- 지원 lazy 로드 of 컨텍스트 컴포넌트
- Implement 컨텍스트 스트리밍 위한 large projects
- Enable 동적 컨텍스트 확장

### 7. 컨텍스트 검증 및 무결성 확인합니다
- Cryptographic 컨텍스트 signatures
- Semantic 일관성 확인
- 버전 compatibility 확인합니다

### 8. 성능 최적화
- Implement efficient 캐싱 mechanisms
- Use probabilistic 데이터 구조 위한 컨텍스트 색인
- Optimize vector search algorithms

## 참조 워크플로우

### 워크플로우 1: Project Resumption
1. Retrieve most 최근 project 컨텍스트
2. Validate 컨텍스트 against 현재 codebase
3. Selectively restore 관련 컴포넌트
4. Generate resumption summary

### 워크플로우 2: Cross-Project 지식 전송
1. Extract semantic vectors 에서 소스 project
2. 맵 및 전송 관련 지식
3. Adapt 컨텍스트 에 target project's 도메인
4. Validate 지식 transferability

## Usage 예제

```bash
# Full context restoration
context-restore project:ai-assistant --mode full

# Incremental context update
context-restore project:web-platform --mode incremental

# Semantic context query
context-restore project:ml-pipeline --query "model training strategy"
```

## 통합 패턴
- RAG (검색 Augmented 세대) 파이프라인
- Multi-에이전트 워크플로우 조정
- Continuous learning 시스템
- 엔터프라이즈 지식 관리

## 미래 Roadmap
- 향상된 multi-modal embedding 지원
- Quantum-inspired vector search algorithms
- Self-healing 컨텍스트 reconstruction
- Adaptive learning 컨텍스트 strategies