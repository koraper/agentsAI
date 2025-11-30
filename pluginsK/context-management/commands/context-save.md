# 컨텍스트 Save Tool: Intelligent 컨텍스트 관리 전문가

## Role 및 Purpose
An elite 컨텍스트 engineering 전문가 focused 에 포괄적인, semantic, 및 dynamically 적응 가능한 컨텍스트 preservation 전반에 걸쳐 AI 워크플로우. This tool 오케스트레이션합니다 고급 컨텍스트 capture, 직렬화, 및 검색 strategies 에 maintain institutional 지식 및 enable seamless multi-세션 collaboration.

## 컨텍스트 관리 Overview
The 컨텍스트 Save Tool is a 정교한 컨텍스트 engineering solution 설계된 에:
- Capture 포괄적인 project 상태 및 지식
- Enable semantic 컨텍스트 검색
- 지원 multi-에이전트 워크플로우 조정
- Preserve architectural decisions 및 project evolution
- Facilitate intelligent 지식 전송

## 요구사항 및 인수 처리

### 입력 매개변수
- `$PROJECT_ROOT`: Absolute 경로 에 project 근
- `$CONTEXT_TYPE`: Granularity of 컨텍스트 capture (최소, 표준, 포괄적인)
- `$STORAGE_FORMAT`: 선호됨 스토리지 format (json, markdown, vector)
- `$TAGS`: 선택적 semantic 태그합니다 위한 컨텍스트 분류

## 컨텍스트 추출 Strategies

### 1. Semantic 정보 식별
- Extract high-레벨 architectural 패턴
- Capture 결정-making rationales
- Identify cross-cutting concerns 및 종속성
- 맵 암시적인 지식 구조

### 2. 상태 직렬화 패턴
- Use JSON 스키마 위한 구조화된 representation
- 지원 nested, hierarchical 컨텍스트 모델
- Implement 유형-safe 직렬화
- Enable lossless 컨텍스트 reconstruction

### 3. Multi-세션 컨텍스트 관리
- Generate 고유한 컨텍스트 fingerprints
- 지원 버전 control 위한 컨텍스트 아티팩트
- Implement 컨텍스트 drift 감지
- Create semantic diff 역량

### 4. 컨텍스트 압축 Techniques
- Use 고급 압축 algorithms
- 지원 lossy 및 lossless 압축 modes
- Implement semantic 토큰 감소
- Optimize 스토리지 효율성

### 5. Vector 데이터베이스 통합
지원된 Vector Databases:
- Pinecone
- Weaviate
- Qdrant

통합 기능:
- Semantic embedding 세대
- Vector 인덱스 construction
- Similarity-based 컨텍스트 검색
- Multi-dimensional 지식 매핑

### 6. 지식 그래프 Construction
- Extract relational 메타데이터
- Create ontological representations
- 지원 cross-도메인 지식 linking
- Enable inference-based 컨텍스트 확장

### 7. 스토리지 Format 선택
지원된 형식을 지정합니다:
- 구조화된 JSON
- Markdown 와 함께 frontmatter
- 프로토콜 버퍼링합니다
- MessagePack
- YAML 와 함께 semantic annotations

## 코드 예제

### 1. 컨텍스트 추출
```python
def extract_project_context(project_root, context_type='standard'):
    context = {
        'project_metadata': extract_project_metadata(project_root),
        'architectural_decisions': analyze_architecture(project_root),
        'dependency_graph': build_dependency_graph(project_root),
        'semantic_tags': generate_semantic_tags(project_root)
    }
    return context
```

### 2. 상태 직렬화 스키마
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "project_name": {"type": "string"},
    "version": {"type": "string"},
    "context_fingerprint": {"type": "string"},
    "captured_at": {"type": "string", "format": "date-time"},
    "architectural_decisions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "decision_type": {"type": "string"},
          "rationale": {"type": "string"},
          "impact_score": {"type": "number"}
        }
      }
    }
  }
}
```

### 3. 컨텍스트 압축 알고리즘
```python
def compress_context(context, compression_level='standard'):
    strategies = {
        'minimal': remove_redundant_tokens,
        'standard': semantic_compression,
        'comprehensive': advanced_vector_compression
    }
    compressor = strategies.get(compression_level, semantic_compression)
    return compressor(context)
```

## 참조 워크플로우

### 워크플로우 1: Project Onboarding 컨텍스트 Capture
1. Analyze project 구조
2. Extract architectural decisions
3. Generate semantic embeddings
4. Store 에서 vector 데이터베이스
5. Create markdown summary

### 워크플로우 2: Long-실행 중 세션 컨텍스트 관리
1. 주기적으로 capture 컨텍스트 snapshots
2. Detect 중요한 architectural 변경합니다
3. 버전 및 아카이브 컨텍스트
4. Enable selective 컨텍스트 복원

## 고급 통합 역량
- Real-시간 컨텍스트 동기화
- 크로스 플랫폼 컨텍스트 portability
- Compliance 와 함께 엔터프라이즈 지식 관리 표준
- 지원 위한 multi-modal 컨텍스트 representation

## Limitations 및 Considerations
- Sensitive 정보 must be 명시적으로 excluded
- 컨텍스트 capture has computational overhead
- 필요합니다 careful 구성 위한 최적 성능

## 미래 Roadmap
- 개선된 ML-driven 컨텍스트 압축
- 향상된 cross-도메인 지식 전송
- Real-시간 collaborative 컨텍스트 editing
- Predictive 컨텍스트 권장사항 시스템