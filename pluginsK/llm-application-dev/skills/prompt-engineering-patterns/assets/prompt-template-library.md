# Prompt 템플릿 라이브러리

## 분류 템플릿

### Sentiment 분석
```
Classify the sentiment of the following text as Positive, Negative, or Neutral.

Text: {text}

Sentiment:
```

### Intent 감지
```
Determine the user's intent from the following message.

Possible intents: {intent_list}

Message: {message}

Intent:
```

### Topic 분류
```
Classify the following article into one of these categories: {categories}

Article:
{article}

Category:
```

## 추출 템플릿

### Named 엔터티 인식
```
Extract all named entities from the text and categorize them.

Text: {text}

Entities (JSON format):
{
  "persons": [],
  "organizations": [],
  "locations": [],
  "dates": []
}
```

### 구조화된 데이터 추출
```
Extract structured information from the job posting.

Job Posting:
{posting}

Extracted Information (JSON):
{
  "title": "",
  "company": "",
  "location": "",
  "salary_range": "",
  "requirements": [],
  "responsibilities": []
}
```

## 세대 템플릿

### Email 세대
```
Write a professional {email_type} email.

To: {recipient}
Context: {context}
Key points to include:
{key_points}

Email:
Subject:
Body:
```

### 코드 세대
```
Generate {language} code for the following task:

Task: {task_description}

Requirements:
{requirements}

Include:
- Error handling
- Input validation
- Inline comments

Code:
```

### Creative 작성
```
Write a {length}-word {style} story about {topic}.

Include these elements:
- {element_1}
- {element_2}
- {element_3}

Story:
```

## 변환 템플릿

### 요약
```
Summarize the following text in {num_sentences} sentences.

Text:
{text}

Summary:
```

### 번역 와 함께 컨텍스트
```
Translate the following {source_lang} text to {target_lang}.

Context: {context}
Tone: {tone}

Text: {text}

Translation:
```

### Format 변환
```
Convert the following {source_format} to {target_format}.

Input:
{input_data}

Output ({target_format}):
```

## 분석 템플릿

### 코드 Review
```
Review the following code for:
1. Bugs and errors
2. Performance issues
3. Security vulnerabilities
4. Best practice violations

Code:
{code}

Review:
```

### SWOT 분석
```
Conduct a SWOT analysis for: {subject}

Context: {context}

Analysis:
Strengths:
-

Weaknesses:
-

Opportunities:
-

Threats:
-
```

## Question Answering 템플릿

### RAG 템플릿
```
Answer the question based on the provided context. If the context doesn't contain enough information, say so.

Context:
{context}

Question: {question}

Answer:
```

### Multi-Turn Q&A
```
Previous conversation:
{conversation_history}

New question: {question}

Answer (continue naturally from conversation):
```

## Specialized 템플릿

### SQL 쿼리 세대
```
Generate a SQL query for the following request.

Database schema:
{schema}

Request: {request}

SQL Query:
```

### Regex 패턴 생성
```
Create a regex pattern to match: {requirement}

Test cases that should match:
{positive_examples}

Test cases that should NOT match:
{negative_examples}

Regex pattern:
```

### API 문서화
```
Generate API documentation for this function:

Code:
{function_code}

Documentation (follow {doc_format} format):
```

## Use these 템플릿 에 의해 filling 에서 the {변수}
