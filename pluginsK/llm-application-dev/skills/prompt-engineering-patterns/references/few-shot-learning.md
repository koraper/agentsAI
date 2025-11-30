# 적은-Shot Learning 가이드

## Overview

적은-shot learning 가능하게 합니다 LLMs 에 perform tasks 에 의해 providing a small 숫자 of 예제 (일반적으로 1-10) 내에 the prompt. This 기법 is 매우 effective 위한 tasks requiring 특정 형식을 지정합니다, 스타일을 지정합니다, 또는 도메인 지식.

## 예제 선택 Strategies

### 1. Semantic Similarity
Select 예제 most similar 에 the 입력 쿼리 사용하여 embedding-based 검색.

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticExampleSelector:
    def __init__(self, examples, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.examples = examples
        self.example_embeddings = self.model.encode([ex['input'] for ex in examples])

    def select(self, query, k=3):
        query_embedding = self.model.encode([query])
        similarities = np.dot(self.example_embeddings, query_embedding.T).flatten()
        top_indices = np.argsort(similarities)[-k:][::-1]
        return [self.examples[i] for i in top_indices]
```

**최선의 위한**: Question answering, text 분류, 추출 tasks

### 2. Diversity Sampling
Maximize coverage of 다른 패턴 및 엣지 cases.

```python
from sklearn.cluster import KMeans

class DiversityExampleSelector:
    def __init__(self, examples, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.examples = examples
        self.embeddings = self.model.encode([ex['input'] for ex in examples])

    def select(self, k=5):
        # Use k-means to find diverse cluster centers
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(self.embeddings)

        # Select example closest to each cluster center
        diverse_examples = []
        for center in kmeans.cluster_centers_:
            distances = np.linalg.norm(self.embeddings - center, axis=1)
            closest_idx = np.argmin(distances)
            diverse_examples.append(self.examples[closest_idx])

        return diverse_examples
```

**최선의 위한**: Demonstrating 작업 variability, 엣지 case 처리

### 3. Difficulty-Based 선택
점진적으로 increase 예제 complexity 에 scaffold learning.

```python
class ProgressiveExampleSelector:
    def __init__(self, examples):
        # Examples should have 'difficulty' scores (0-1)
        self.examples = sorted(examples, key=lambda x: x['difficulty'])

    def select(self, k=3):
        # Select examples with linearly increasing difficulty
        step = len(self.examples) // k
        return [self.examples[i * step] for i in range(k)]
```

**최선의 위한**: 복잡한 reasoning tasks, 코드 세대

### 4. 오류-Based 선택
Include 예제 것 주소 일반적인 실패 modes.

```python
class ErrorGuidedSelector:
    def __init__(self, examples, error_patterns):
        self.examples = examples
        self.error_patterns = error_patterns  # Common mistakes to avoid

    def select(self, query, k=3):
        # Select examples demonstrating correct handling of error patterns
        selected = []
        for pattern in self.error_patterns[:k]:
            matching = [ex for ex in self.examples if pattern in ex['demonstrates']]
            if matching:
                selected.append(matching[0])
        return selected
```

**최선의 위한**: Tasks 와 함께 known 실패 패턴, safety-긴급 애플리케이션

## 예제 Construction 최선의 관행

### Format 일관성
모든 예제 should follow identical 형식 지정:

```python
# Good: Consistent format
examples = [
    {
        "input": "What is the capital of France?",
        "output": "Paris"
    },
    {
        "input": "What is the capital of Germany?",
        "output": "Berlin"
    }
]

# Bad: Inconsistent format
examples = [
    "Q: What is the capital of France? A: Paris",
    {"question": "What is the capital of Germany?", "answer": "Berlin"}
]
```

### 입력-출력 정렬
Ensure 예제 demonstrate the exact 작업 you want the 모델 에 perform:

```python
# Good: Clear input-output relationship
example = {
    "input": "Sentiment: The movie was terrible and boring.",
    "output": "Negative"
}

# Bad: Ambiguous relationship
example = {
    "input": "The movie was terrible and boring.",
    "output": "This review expresses negative sentiment toward the film."
}
```

### Complexity Balance
Include 예제 spanning the 예상되는 difficulty 범위:

```python
examples = [
    # Simple case
    {"input": "2 + 2", "output": "4"},

    # Moderate case
    {"input": "15 * 3 + 8", "output": "53"},

    # Complex case
    {"input": "(12 + 8) * 3 - 15 / 5", "output": "57"}
]
```

## 컨텍스트 Window 관리

### 토큰 Budget Allocation
일반적인 배포 위한 a 4K 컨텍스트 window:

```
System Prompt:        500 tokens  (12%)
Few-Shot Examples:   1500 tokens  (38%)
User Input:           500 tokens  (12%)
Response:            1500 tokens  (38%)
```

### 동적 예제 Truncation
```python
class TokenAwareSelector:
    def __init__(self, examples, tokenizer, max_tokens=1500):
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens

    def select(self, query, k=5):
        selected = []
        total_tokens = 0

        # Start with most relevant examples
        candidates = self.rank_by_relevance(query)

        for example in candidates[:k]:
            example_tokens = len(self.tokenizer.encode(
                f"Input: {example['input']}\nOutput: {example['output']}\n\n"
            ))

            if total_tokens + example_tokens <= self.max_tokens:
                selected.append(example)
                total_tokens += example_tokens
            else:
                break

        return selected
```

## 엣지 case 처리

### Include 경계 예제
```python
edge_case_examples = [
    # Empty input
    {"input": "", "output": "Please provide input text."},

    # Very long input (truncated in example)
    {"input": "..." + "word " * 1000, "output": "Input exceeds maximum length."},

    # Ambiguous input
    {"input": "bank", "output": "Ambiguous: Could refer to financial institution or river bank."},

    # Invalid input
    {"input": "!@#$%", "output": "Invalid input format. Please provide valid text."}
]
```

## 적은-Shot Prompt 템플릿

### 분류 템플릿
```python
def build_classification_prompt(examples, query, labels):
    prompt = f"Classify the text into one of these categories: {', '.join(labels)}\n\n"

    for ex in examples:
        prompt += f"Text: {ex['input']}\nCategory: {ex['output']}\n\n"

    prompt += f"Text: {query}\nCategory:"
    return prompt
```

### 추출 템플릿
```python
def build_extraction_prompt(examples, query):
    prompt = "Extract structured information from the text.\n\n"

    for ex in examples:
        prompt += f"Text: {ex['input']}\nExtracted: {json.dumps(ex['output'])}\n\n"

    prompt += f"Text: {query}\nExtracted:"
    return prompt
```

### 변환 템플릿
```python
def build_transformation_prompt(examples, query):
    prompt = "Transform the input according to the pattern shown in examples.\n\n"

    for ex in examples:
        prompt += f"Input: {ex['input']}\nOutput: {ex['output']}\n\n"

    prompt += f"Input: {query}\nOutput:"
    return prompt
```

## 평가 및 최적화

### 예제 품질 메트릭
```python
def evaluate_example_quality(example, validation_set):
    metrics = {
        'clarity': rate_clarity(example),  # 0-1 score
        'representativeness': calculate_similarity_to_validation(example, validation_set),
        'difficulty': estimate_difficulty(example),
        'uniqueness': calculate_uniqueness(example, other_examples)
    }
    return metrics
```

### A/B 테스트 예제 세트
```python
class ExampleSetTester:
    def __init__(self, llm_client):
        self.client = llm_client

    def compare_example_sets(self, set_a, set_b, test_queries):
        results_a = self.evaluate_set(set_a, test_queries)
        results_b = self.evaluate_set(set_b, test_queries)

        return {
            'set_a_accuracy': results_a['accuracy'],
            'set_b_accuracy': results_b['accuracy'],
            'winner': 'A' if results_a['accuracy'] > results_b['accuracy'] else 'B',
            'improvement': abs(results_a['accuracy'] - results_b['accuracy'])
        }

    def evaluate_set(self, examples, test_queries):
        correct = 0
        for query in test_queries:
            prompt = build_prompt(examples, query['input'])
            response = self.client.complete(prompt)
            if response == query['expected_output']:
                correct += 1
        return {'accuracy': correct / len(test_queries)}
```

## 고급 Techniques

### Meta-Learning (Learning 에 Select)
Train a small 모델 에 predict 어느 예제 will be most effective:

```python
from sklearn.ensemble import RandomForestClassifier

class LearnedExampleSelector:
    def __init__(self):
        self.selector_model = RandomForestClassifier()

    def train(self, training_data):
        # training_data: list of (query, example, success) tuples
        features = []
        labels = []

        for query, example, success in training_data:
            features.append(self.extract_features(query, example))
            labels.append(1 if success else 0)

        self.selector_model.fit(features, labels)

    def extract_features(self, query, example):
        return [
            semantic_similarity(query, example['input']),
            len(example['input']),
            len(example['output']),
            keyword_overlap(query, example['input'])
        ]

    def select(self, query, candidates, k=3):
        scores = []
        for example in candidates:
            features = self.extract_features(query, example)
            score = self.selector_model.predict_proba([features])[0][1]
            scores.append((score, example))

        return [ex for _, ex in sorted(scores, reverse=True)[:k]]
```

### Adaptive 예제 개수
Dynamically adjust the 숫자 of 예제 based 에 작업 difficulty:

```python
class AdaptiveExampleSelector:
    def __init__(self, examples):
        self.examples = examples

    def select(self, query, max_examples=5):
        # Start with 1 example
        for k in range(1, max_examples + 1):
            selected = self.get_top_k(query, k)

            # Quick confidence check (could use a lightweight model)
            if self.estimated_confidence(query, selected) > 0.9:
                return selected

        return selected  # Return max_examples if never confident enough
```

## 일반적인 Mistakes

1. **또한 많은 예제**: More isn't 항상 더 나은; can dilute focus
2. **Irrelevant 예제**: 예제 should match the target 작업 밀접하게
3. **일관되지 않은 형식 지정**: Confuses the 모델 약 출력 format
4. **Overfitting 에 예제**: 모델 copies 예제 패턴 또한 literally
5. **Ignoring 토큰 제한합니다**: 실행 중 out of 공간 위한 actual 입력/출력

## 리소스

- 예제 dataset repositories
- Pre-구축된 예제 selectors 위한 일반적인 tasks
- 평가 프레임워크 위한 적은-shot 성능
- 토큰 계산 utilities 위한 다른 모델
