---
name: prompt-engineering-patterns
description: 마스터 고급 prompt engineering techniques 에 maximize LLM 성능, 신뢰성, 및 controllability 에서 production. Use 때 optimizing prompts, improving LLM 출력, 또는 designing production prompt 템플릿.
---

# Prompt Engineering 패턴

마스터 고급 prompt engineering techniques 에 maximize LLM 성능, 신뢰성, 및 controllability.

## 때 에 Use This Skill

- Designing 복잡한 prompts 위한 production LLM 애플리케이션
- Optimizing prompt 성능 및 일관성
- Implementing 구조화된 reasoning 패턴 (chain-of-thought, 트리-of-thought)
- 구축 적은-shot learning 시스템 와 함께 동적 예제 선택
- 생성하는 reusable prompt 템플릿 와 함께 가변 interpolation
- 디버깅 및 refining prompts 것 produce 일관되지 않은 출력
- Implementing 시스템 prompts 위한 specialized AI assistants

## 핵심 역량

### 1. 적은-Shot Learning
- 예제 선택 strategies (semantic similarity, diversity sampling)
- 균형 예제 개수 와 함께 컨텍스트 window constraints
- Constructing effective demonstrations 와 함께 입력-출력 쌍
- 동적 예제 검색 에서 지식 기초
- 처리 엣지 cases 통해 strategic 예제 선택

### 2. Chain-of-Thought Prompting
- 단계-에 의해-단계 reasoning elicitation
- Zero-shot CoT 와 함께 "Let's think 단계 에 의해 단계"
- 적은-shot CoT 와 함께 reasoning 추적합니다
- Self-일관성 techniques (sampling 여러 reasoning 경로)
- 확인 및 검증 steps

### 3. Prompt 최적화
- Iterative refinement 워크플로우
- A/B 테스트 prompt variations
- Measuring prompt 성능 메트릭 (정확성, 일관성, 지연 시간)
- Reducing 토큰 usage 동안 maintaining 품질
- 처리 엣지 cases 및 실패 modes

### 4. 템플릿 시스템
- 가변 interpolation 및 형식 지정
- Conditional prompt sections
- Multi-turn conversation 템플릿
- Role-based prompt composition
- 모듈식 prompt 컴포넌트

### 5. 시스템 Prompt 설계
- Setting 모델 behavior 및 constraints
- Defining 출력 형식을 지정합니다 및 구조
- Establishing role 및 expertise
- Safety 가이드라인 및 콘텐츠 정책
- 컨텍스트 setting 및 background 정보

## Quick Start

```python
from prompt_optimizer import PromptTemplate, FewShotSelector

# Define a structured prompt template
template = PromptTemplate(
    system="You are an expert SQL developer. Generate efficient, secure SQL queries.",
    instruction="Convert the following natural language query to SQL:\n{query}",
    few_shot_examples=True,
    output_format="SQL code block with explanatory comments"
)

# Configure few-shot learning
selector = FewShotSelector(
    examples_db="sql_examples.jsonl",
    selection_strategy="semantic_similarity",
    max_examples=3
)

# Generate optimized prompt
prompt = template.render(
    query="Find all users who registered in the last 30 days",
    examples=selector.select(query="user registration date filter")
)
```

## 키 패턴

### Progressive Disclosure
Start 와 함께 간단한 prompts, add complexity 오직 때 필요한:

1. **레벨 1**: 직접 지시
   - "Summarize this article"

2. **레벨 2**: Add constraints
   - "Summarize this article 에서 3 bullet points, focusing 에 키 findings"

3. **레벨 3**: Add reasoning
   - "읽은 this article, identify the main findings, then summarize 에서 3 bullet points"

4. **레벨 4**: Add 예제
   - Include 2-3 예제 summaries 와 함께 입력-출력 쌍

### 지시 계층
```
[System Context] → [Task Instruction] → [Examples] → [Input Data] → [Output Format]
```

### 오류 복구
빌드 prompts 것 gracefully handle 실패:
- Include fallback 지시사항
- 요청 confidence 점수를 매깁니다
- Ask 위한 alternative interpretations 때 불확실한
- Specify 어떻게 에 indicate missing 정보

## 최선의 관행

1. **Be 특정**: Vague prompts produce 일관되지 않은 results
2. **Show, Don't Tell**: 예제 are more effective 보다 descriptions
3. **Test 광범위하게**: Evaluate 에 diverse, representative 입력
4. **Iterate 빠르게**: Small 변경합니다 can have large impacts
5. **모니터 성능**: Track 메트릭 에서 production
6. **버전 Control**: Treat prompts 처럼 코드 와 함께 적절한 versioning
7. **Document Intent**: Explain 왜 prompts are 구조화된 처럼 they are

## 일반적인 Pitfalls

- **Over-engineering**: 시작하는 와 함께 복잡한 prompts 이전 trying 간단한 ones
- **예제 pollution**: 사용하여 예제 것 don't match the target 작업
- **컨텍스트 overflow**: Exceeding 토큰 제한합니다 와 함께 과도한 예제
- **애매한 지시사항**: Leaving room 위한 여러 interpretations
- **Ignoring 엣지 cases**: Not 테스트 에 특이한 또는 경계 입력

## 통합 패턴

### 와 함께 RAG 시스템
```python
# Combine retrieved context with prompt engineering
prompt = f"""Given the following context:
{retrieved_context}

{few_shot_examples}

Question: {user_question}

Provide a detailed answer based solely on the context above. If the context doesn't contain enough information, explicitly state what's missing."""
```

### 와 함께 검증
```python
# Add self-verification step
prompt = f"""{main_task_prompt}

After generating your response, verify it meets these criteria:
1. Answers the question directly
2. Uses only information from provided context
3. Cites specific sources
4. Acknowledges any uncertainty

If verification fails, revise your response."""
```

## 성능 최적화

### 토큰 효율성
- Remove 중복된 words 및 phrases
- Use abbreviations consistently 이후 첫 번째 정의
- Consolidate similar 지시사항
- Move 안정적인 콘텐츠 에 시스템 prompts

### 지연 시간 감소
- Minimize prompt length 없이 sacrificing 품질
- Use 스트리밍 위한 long-폼 출력
- 캐시 일반적인 prompt prefixes
- Batch similar 요청 때 possible

## 리소스

- **참조/적은-shot-learning.md**: Deep dive 에 예제 선택 및 construction
- **참조/chain-of-thought.md**: 고급 reasoning elicitation techniques
- **참조/prompt-최적화.md**: Systematic refinement 워크플로우
- **참조/prompt-템플릿.md**: Reusable 템플릿 패턴
- **참조/시스템-prompts.md**: 시스템-레벨 prompt 설계
- **자산/prompt-템플릿-라이브러리.md**: 검증된 prompt 템플릿
- **자산/적은-shot-예제.json**: Curated 예제 datasets
- **스크립트/optimize-prompt.py**: 자동화된 prompt 최적화 tool

## Success 메트릭

Track these KPIs 위한 your prompts:
- **정확성**: 정확성 of 출력
- **일관성**: Reproducibility 전반에 걸쳐 similar 입력
- **지연 시간**: 응답 시간 (P50, P95, P99)
- **토큰 Usage**: 평균 토큰 per 요청
- **Success Rate**: 백분율 of 유효한 출력
- **사용자 Satisfaction**: Ratings 및 feedback

## 다음 Steps

1. Review the prompt 템플릿 라이브러리 위한 일반적인 패턴
2. Experiment 와 함께 적은-shot learning 위한 your 특정 use case
3. Implement prompt versioning 및 A/B 테스트
4. 세트 up 자동화된 평가 파이프라인
5. Document your prompt engineering decisions 및 learnings
