---
name: llm-evaluation
description: Implement 포괄적인 평가 strategies 위한 LLM 애플리케이션 사용하여 자동화된 메트릭, human feedback, 및 benchmarking. Use 때 테스트 LLM 성능, measuring AI 애플리케이션 품질, 또는 establishing 평가 프레임워크.
---

# LLM 평가

마스터 포괄적인 평가 strategies 위한 LLM 애플리케이션, 에서 자동화된 메트릭 에 human 평가 및 A/B 테스트.

## 때 에 Use This Skill

- Measuring LLM 애플리케이션 성능 systematically
- Comparing 다른 모델 또는 prompts
- Detecting 성능 regressions 이전 배포
- Validating improvements 에서 prompt 변경합니다
- 구축 confidence 에서 production 시스템
- Establishing baselines 및 추적 진행 over 시간
- 디버깅 unexpected 모델 behavior

## 핵심 평가 유형

### 1. 자동화된 메트릭
Fast, repeatable, scalable 평가 사용하여 계산된 점수를 매깁니다.

**Text 세대:**
- **BLEU**: N-gram overlap (번역)
- **ROUGE**: Recall-oriented (요약)
- **METEOR**: Semantic similarity
- **BERTScore**: Embedding-based similarity
- **Perplexity**: Language 모델 confidence

**분류:**
- **정확성**: 백분율 올바른
- **정밀도/Recall/F1**: 클래스-특정 성능
- **Confusion 매트릭스**: 오류 패턴
- **AUC-ROC**: 순위 품질

**검색 (RAG):**
- **MRR**: 평균 Reciprocal Rank
- **NDCG**: 정규화된 Discounted Cumulative Gain
- **정밀도@K**: 관련 에서 top K
- **Recall@K**: Coverage 에서 top K

### 2. Human 평가
Manual 평가 위한 품질 aspects 어려운 에 automate.

**Dimensions:**
- **정확성**: Factual 정확성
- **일관성**: 논리적인 흐름
- **Relevance**: Answers the question
- **Fluency**: Natural language 품질
- **Safety**: 아니요 harmful 콘텐츠
- **Helpfulness**: Useful 에 the 사용자

### 3. LLM-처럼-Judge
Use stronger LLMs 에 evaluate weaker 모델 출력.

**Approaches:**
- **Pointwise**: Score 개별 응답
- **Pairwise**: Compare two 응답
- **참조-based**: Compare 에 gold 표준
- **참조-무료**: Judge 없이 ground truth

## Quick Start

```python
from llm_eval import EvaluationSuite, Metric

# Define evaluation suite
suite = EvaluationSuite([
    Metric.accuracy(),
    Metric.bleu(),
    Metric.bertscore(),
    Metric.custom(name="groundedness", fn=check_groundedness)
])

# Prepare test cases
test_cases = [
    {
        "input": "What is the capital of France?",
        "expected": "Paris",
        "context": "France is a country in Europe. Paris is its capital."
    },
    # ... more test cases
]

# Run evaluation
results = suite.evaluate(
    model=your_model,
    test_cases=test_cases
)

print(f"Overall Accuracy: {results.metrics['accuracy']}")
print(f"BLEU Score: {results.metrics['bleu']}")
```

## 자동화된 메트릭 구현

### BLEU Score
```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def calculate_bleu(reference, hypothesis):
    """Calculate BLEU score between reference and hypothesis."""
    smoothie = SmoothingFunction().method4

    return sentence_bleu(
        [reference.split()],
        hypothesis.split(),
        smoothing_function=smoothie
    )

# Usage
bleu = calculate_bleu(
    reference="The cat sat on the mat",
    hypothesis="A cat is sitting on the mat"
)
```

### ROUGE Score
```python
from rouge_score import rouge_scorer

def calculate_rouge(reference, hypothesis):
    """Calculate ROUGE scores."""
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)

    return {
        'rouge1': scores['rouge1'].fmeasure,
        'rouge2': scores['rouge2'].fmeasure,
        'rougeL': scores['rougeL'].fmeasure
    }
```

### BERTScore
```python
from bert_score import score

def calculate_bertscore(references, hypotheses):
    """Calculate BERTScore using pre-trained BERT."""
    P, R, F1 = score(
        hypotheses,
        references,
        lang='en',
        model_type='microsoft/deberta-xlarge-mnli'
    )

    return {
        'precision': P.mean().item(),
        'recall': R.mean().item(),
        'f1': F1.mean().item()
    }
```

### 사용자 정의 메트릭
```python
def calculate_groundedness(response, context):
    """Check if response is grounded in provided context."""
    # Use NLI model to check entailment
    from transformers import pipeline

    nli = pipeline("text-classification", model="microsoft/deberta-large-mnli")

    result = nli(f"{context} [SEP] {response}")[0]

    # Return confidence that response is entailed by context
    return result['score'] if result['label'] == 'ENTAILMENT' else 0.0

def calculate_toxicity(text):
    """Measure toxicity in generated text."""
    from detoxify import Detoxify

    results = Detoxify('original').predict(text)
    return max(results.values())  # Return highest toxicity score

def calculate_factuality(claim, knowledge_base):
    """Verify factual claims against knowledge base."""
    # Implementation depends on your knowledge base
    # Could use retrieval + NLI, or fact-checking API
    pass
```

## LLM-처럼-Judge 패턴

### Single 출력 평가
```python
def llm_judge_quality(response, question):
    """Use GPT-5 to judge response quality."""
    prompt = f"""Rate the following response on a scale of 1-10 for:
1. Accuracy (factually correct)
2. Helpfulness (answers the question)
3. Clarity (well-written and understandable)

Question: {question}
Response: {response}

Provide ratings in JSON format:
{{
  "accuracy": <1-10>,
  "helpfulness": <1-10>,
  "clarity": <1-10>,
  "reasoning": "<brief explanation>"
}}
"""

    result = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(result.choices[0].message.content)
```

### Pairwise 비교
```python
def compare_responses(question, response_a, response_b):
    """Compare two responses using LLM judge."""
    prompt = f"""Compare these two responses to the question and determine which is better.

Question: {question}

Response A: {response_a}

Response B: {response_b}

Which response is better and why? Consider accuracy, helpfulness, and clarity.

Answer with JSON:
{{
  "winner": "A" or "B" or "tie",
  "reasoning": "<explanation>",
  "confidence": <1-10>
}}
"""

    result = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(result.choices[0].message.content)
```

## Human 평가 프레임워크

### 주석 가이드라인
```python
class AnnotationTask:
    """Structure for human annotation task."""

    def __init__(self, response, question, context=None):
        self.response = response
        self.question = question
        self.context = context

    def get_annotation_form(self):
        return {
            "question": self.question,
            "context": self.context,
            "response": self.response,
            "ratings": {
                "accuracy": {
                    "scale": "1-5",
                    "description": "Is the response factually correct?"
                },
                "relevance": {
                    "scale": "1-5",
                    "description": "Does it answer the question?"
                },
                "coherence": {
                    "scale": "1-5",
                    "description": "Is it logically consistent?"
                }
            },
            "issues": {
                "factual_error": False,
                "hallucination": False,
                "off_topic": False,
                "unsafe_content": False
            },
            "feedback": ""
        }
```

### Inter-Rater Agreement
```python
from sklearn.metrics import cohen_kappa_score

def calculate_agreement(rater1_scores, rater2_scores):
    """Calculate inter-rater agreement."""
    kappa = cohen_kappa_score(rater1_scores, rater2_scores)

    interpretation = {
        kappa < 0: "Poor",
        kappa < 0.2: "Slight",
        kappa < 0.4: "Fair",
        kappa < 0.6: "Moderate",
        kappa < 0.8: "Substantial",
        kappa <= 1.0: "Almost Perfect"
    }

    return {
        "kappa": kappa,
        "interpretation": interpretation[True]
    }
```

## A/B 테스트

### Statistical 테스트 프레임워크
```python
from scipy import stats
import numpy as np

class ABTest:
    def __init__(self, variant_a_name="A", variant_b_name="B"):
        self.variant_a = {"name": variant_a_name, "scores": []}
        self.variant_b = {"name": variant_b_name, "scores": []}

    def add_result(self, variant, score):
        """Add evaluation result for a variant."""
        if variant == "A":
            self.variant_a["scores"].append(score)
        else:
            self.variant_b["scores"].append(score)

    def analyze(self, alpha=0.05):
        """Perform statistical analysis."""
        a_scores = self.variant_a["scores"]
        b_scores = self.variant_b["scores"]

        # T-test
        t_stat, p_value = stats.ttest_ind(a_scores, b_scores)

        # Effect size (Cohen's d)
        pooled_std = np.sqrt((np.std(a_scores)**2 + np.std(b_scores)**2) / 2)
        cohens_d = (np.mean(b_scores) - np.mean(a_scores)) / pooled_std

        return {
            "variant_a_mean": np.mean(a_scores),
            "variant_b_mean": np.mean(b_scores),
            "difference": np.mean(b_scores) - np.mean(a_scores),
            "relative_improvement": (np.mean(b_scores) - np.mean(a_scores)) / np.mean(a_scores),
            "p_value": p_value,
            "statistically_significant": p_value < alpha,
            "cohens_d": cohens_d,
            "effect_size": self.interpret_cohens_d(cohens_d),
            "winner": "B" if np.mean(b_scores) > np.mean(a_scores) else "A"
        }

    @staticmethod
    def interpret_cohens_d(d):
        """Interpret Cohen's d effect size."""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"
```

## Regression 테스트

### Regression 감지
```python
class RegressionDetector:
    def __init__(self, baseline_results, threshold=0.05):
        self.baseline = baseline_results
        self.threshold = threshold

    def check_for_regression(self, new_results):
        """Detect if new results show regression."""
        regressions = []

        for metric in self.baseline.keys():
            baseline_score = self.baseline[metric]
            new_score = new_results.get(metric)

            if new_score is None:
                continue

            # Calculate relative change
            relative_change = (new_score - baseline_score) / baseline_score

            # Flag if significant decrease
            if relative_change < -self.threshold:
                regressions.append({
                    "metric": metric,
                    "baseline": baseline_score,
                    "current": new_score,
                    "change": relative_change
                })

        return {
            "has_regression": len(regressions) > 0,
            "regressions": regressions
        }
```

## Benchmarking

### 실행 중 Benchmarks
```python
class BenchmarkRunner:
    def __init__(self, benchmark_dataset):
        self.dataset = benchmark_dataset

    def run_benchmark(self, model, metrics):
        """Run model on benchmark and calculate metrics."""
        results = {metric.name: [] for metric in metrics}

        for example in self.dataset:
            # Generate prediction
            prediction = model.predict(example["input"])

            # Calculate each metric
            for metric in metrics:
                score = metric.calculate(
                    prediction=prediction,
                    reference=example["reference"],
                    context=example.get("context")
                )
                results[metric.name].append(score)

        # Aggregate results
        return {
            metric: {
                "mean": np.mean(scores),
                "std": np.std(scores),
                "min": min(scores),
                "max": max(scores)
            }
            for metric, scores in results.items()
        }
```

## 리소스

- **참조/메트릭.md**: 포괄적인 metric 가이드
- **참조/human-평가.md**: 주석 최선의 관행
- **참조/benchmarking.md**: 표준 benchmarks
- **참조/a-b-테스트.md**: Statistical 테스트 가이드
- **참조/regression-테스트.md**: CI/CD 통합
- **자산/평가-프레임워크.py**: 완전한 평가 harness
- **자산/benchmark-dataset.jsonl**: 예제 datasets
- **스크립트/evaluate-모델.py**: 자동화된 평가 runner

## 최선의 관행

1. **여러 메트릭**: Use diverse 메트릭 위한 포괄적인 뷰
2. **Representative 데이터**: Test 에 real-세계, diverse 예제
3. **Baselines**: 항상 compare against baseline 성능
4. **Statistical Rigor**: Use 적절한 statistical 테스트합니다 위한 comparisons
5. **Continuous 평가**: Integrate into CI/CD 파이프라인
6. **Human 검증**: Combine 자동화된 메트릭 와 함께 human judgment
7. **오류 분석**: Investigate 실패 에 understand weaknesses
8. **버전 Control**: Track 평가 results over 시간

## 일반적인 Pitfalls

- **Single Metric Obsession**: Optimizing 위한 one metric 에서 the expense of others
- **Small 샘플 Size**: Drawing conclusions 에서 또한 적은 예제
- **데이터 Contamination**: 테스트 에 training 데이터
- **Ignoring 분산**: Not accounting 위한 statistical uncertainty
- **Metric Mismatch**: 사용하여 메트릭 not 정렬된 와 함께 비즈니스 goals
