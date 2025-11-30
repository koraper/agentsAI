---
name: langchain-architecture
description: 설계 LLM 애플리케이션 사용하여 the LangChain 프레임워크 와 함께 에이전트, 메모리, 및 tool 통합 패턴. Use 때 구축 LangChain 애플리케이션, implementing AI 에이전트, 또는 생성하는 복잡한 LLM 워크플로우.
---

# LangChain 아키텍처

마스터 the LangChain 프레임워크 위한 구축 정교한 LLM 애플리케이션 와 함께 에이전트, chains, 메모리, 및 tool 통합.

## 때 에 Use This Skill

- 구축 autonomous AI 에이전트 와 함께 tool access
- Implementing 복잡한 multi-단계 LLM 워크플로우
- Managing conversation 메모리 및 상태
- Integrating LLMs 와 함께 외부 데이터 sources 및 APIs
- 생성하는 모듈식, reusable LLM 애플리케이션 컴포넌트
- Implementing document 처리 파이프라인
- 구축 production-grade LLM 애플리케이션

## 핵심 개념

### 1. 에이전트
Autonomous 시스템 것 use LLMs 에 decide 어느 actions 에 take.

**에이전트 유형:**
- **ReAct**: Reasoning + Acting 에서 interleaved 방식
- **OpenAI 함수**: Leverages 함수 calling API
- **구조화된 Chat**: 처리합니다 multi-입력 tools
- **Conversational**: 최적화된 위한 chat 인터페이스
- **Self-Ask 와 함께 Search**: 분해합니다 복잡한 쿼리

### 2. Chains
순서를 정합니다 of calls 에 LLMs 또는 other utilities.

**Chain 유형:**
- **LLMChain**: 기본 prompt + LLM combination
- **SequentialChain**: 여러 chains 에서 시퀀스
- **RouterChain**: 라우트 입력 에 specialized chains
- **TransformChain**: 데이터 transformations 사이 steps
- **MapReduceChain**: 병렬로 처리 와 함께 집계

### 3. 메모리
시스템 위한 maintaining 컨텍스트 전반에 걸쳐 interactions.

**메모리 유형:**
- **ConversationBufferMemory**: 저장합니다 모든 메시지
- **ConversationSummaryMemory**: 요약합니다 older 메시지
- **ConversationBufferWindowMemory**: Keeps 마지막 N 메시지
- **EntityMemory**: 추적합니다 정보 약 엔터티
- **VectorStoreMemory**: Semantic similarity 검색

### 4. Document 처리
로드, transforming, 및 storing 문서화합니다 위한 검색.

**컴포넌트:**
- **Document Loaders**: Load 에서 various sources
- **Text Splitters**: Chunk 문서화합니다 intelligently
- **Vector 저장합니다**: Store 및 retrieve embeddings
- **Retrievers**: Fetch 관련 문서화합니다
- **인덱스**: Organize 문서화합니다 위한 efficient access

### 5. Callbacks
Hooks 위한 로깅, 모니터링, 및 디버깅.

**Use Cases:**
- 요청/응답 로깅
- 토큰 usage 추적
- 지연 시간 모니터링
- 오류 처리
- 사용자 정의 메트릭 컬렉션

## Quick Start

```python
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

# Initialize LLM
llm = OpenAI(temperature=0)

# Load tools
tools = load_tools(["serpapi", "llm-math"], llm=llm)

# Add memory
memory = ConversationBufferMemory(memory_key="chat_history")

# Create agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# Run agent
result = agent.run("What's the weather in SF? Then calculate 25 * 4")
```

## 아키텍처 패턴

### 패턴 1: RAG 와 함께 LangChain
```python
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Load and process documents
loader = TextLoader('documents.txt')
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)

# Create retrieval chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Query
result = qa_chain({"query": "What is the main topic?"})
```

### 패턴 2: 사용자 정의 에이전트 와 함께 Tools
```python
from langchain.agents import Tool, AgentExecutor
from langchain.agents.react.base import ReActDocstoreAgent
from langchain.tools import tool

@tool
def search_database(query: str) -> str:
    """Search internal database for information."""
    # Your database search logic
    return f"Results for: {query}"

@tool
def send_email(recipient: str, content: str) -> str:
    """Send an email to specified recipient."""
    # Email sending logic
    return f"Email sent to {recipient}"

tools = [search_database, send_email]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
```

### 패턴 3: Multi-단계 Chain
```python
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate

# Step 1: Extract key information
extract_prompt = PromptTemplate(
    input_variables=["text"],
    template="Extract key entities from: {text}\n\nEntities:"
)
extract_chain = LLMChain(llm=llm, prompt=extract_prompt, output_key="entities")

# Step 2: Analyze entities
analyze_prompt = PromptTemplate(
    input_variables=["entities"],
    template="Analyze these entities: {entities}\n\nAnalysis:"
)
analyze_chain = LLMChain(llm=llm, prompt=analyze_prompt, output_key="analysis")

# Step 3: Generate summary
summary_prompt = PromptTemplate(
    input_variables=["entities", "analysis"],
    template="Summarize:\nEntities: {entities}\nAnalysis: {analysis}\n\nSummary:"
)
summary_chain = LLMChain(llm=llm, prompt=summary_prompt, output_key="summary")

# Combine into sequential chain
overall_chain = SequentialChain(
    chains=[extract_chain, analyze_chain, summary_chain],
    input_variables=["text"],
    output_variables=["entities", "analysis", "summary"],
    verbose=True
)
```

## 메모리 관리 최선의 관행

### 선택하는 the 맞는 메모리 유형
```python
# For short conversations (< 10 messages)
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()

# For long conversations (summarize old messages)
from langchain.memory import ConversationSummaryMemory
memory = ConversationSummaryMemory(llm=llm)

# For sliding window (last N messages)
from langchain.memory import ConversationBufferWindowMemory
memory = ConversationBufferWindowMemory(k=5)

# For entity tracking
from langchain.memory import ConversationEntityMemory
memory = ConversationEntityMemory(llm=llm)

# For semantic retrieval of relevant history
from langchain.memory import VectorStoreRetrieverMemory
memory = VectorStoreRetrieverMemory(retriever=retriever)
```

## 콜백 시스템

### 사용자 정의 콜백 핸들러
```python
from langchain.callbacks.base import BaseCallbackHandler

class CustomCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"LLM started with prompts: {prompts}")

    def on_llm_end(self, response, **kwargs):
        print(f"LLM ended with response: {response}")

    def on_llm_error(self, error, **kwargs):
        print(f"LLM error: {error}")

    def on_chain_start(self, serialized, inputs, **kwargs):
        print(f"Chain started with inputs: {inputs}")

    def on_agent_action(self, action, **kwargs):
        print(f"Agent taking action: {action}")

# Use callback
agent.run("query", callbacks=[CustomCallbackHandler()])
```

## 테스트 Strategies

```python
import pytest
from unittest.mock import Mock

def test_agent_tool_selection():
    # Mock LLM to return specific tool selection
    mock_llm = Mock()
    mock_llm.predict.return_value = "Action: search_database\nAction Input: test query"

    agent = initialize_agent(tools, mock_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

    result = agent.run("test query")

    # Verify correct tool was selected
    assert "search_database" in str(mock_llm.predict.call_args)

def test_memory_persistence():
    memory = ConversationBufferMemory()

    memory.save_context({"input": "Hi"}, {"output": "Hello!"})

    assert "Hi" in memory.load_memory_variables({})['history']
    assert "Hello!" in memory.load_memory_variables({})['history']
```

## 성능 최적화

### 1. 캐싱
```python
from langchain.cache import InMemoryCache
import langchain

langchain.llm_cache = InMemoryCache()
```

### 2. Batch 처리
```python
# Process multiple documents in parallel
from langchain.document_loaders import DirectoryLoader
from concurrent.futures import ThreadPoolExecutor

loader = DirectoryLoader('./docs')
docs = loader.load()

def process_doc(doc):
    return text_splitter.split_documents([doc])

with ThreadPoolExecutor(max_workers=4) as executor:
    split_docs = list(executor.map(process_doc, docs))
```

### 3. 스트리밍 응답
```python
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = OpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()])
```

## 리소스

- **참조/에이전트.md**: Deep dive 에 에이전트 아키텍처
- **참조/메모리.md**: 메모리 시스템 패턴
- **참조/chains.md**: Chain composition strategies
- **참조/document-처리.md**: Document 로드 및 색인
- **참조/callbacks.md**: 모니터링 및 observability
- **자산/에이전트-템플릿.py**: 프로덕션 준비 완료 에이전트 템플릿
- **자산/메모리-config.yaml**: 메모리 구성 예제
- **자산/chain-예제.py**: 복잡한 chain 예제

## 일반적인 Pitfalls

1. **메모리 Overflow**: Not managing conversation history length
2. **Tool 선택 오류**: Poor tool descriptions confuse 에이전트
3. **컨텍스트 Window Exceeded**: Exceeding LLM 토큰 제한합니다
4. **아니요 오류 처리**: Not catching 및 처리 에이전트 실패
5. **Inefficient 검색**: Not optimizing vector store 쿼리

## Production Checklist

- [ ] Implement 적절한 오류 처리
- [ ] Add 요청/응답 로깅
- [ ] 모니터 토큰 usage 및 costs
- [ ] 세트 타임아웃 제한합니다 위한 에이전트 실행
- [ ] Implement 속도 제한
- [ ] Add 입력 검증
- [ ] Test 와 함께 엣지 cases
- [ ] 세트 up observability (callbacks)
- [ ] Implement fallback strategies
- [ ] 버전 control prompts 및 configurations
