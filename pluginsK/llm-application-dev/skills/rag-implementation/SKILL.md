---
name: rag-implementation
description: 빌드 검색-Augmented 세대 (RAG) 시스템 위한 LLM 애플리케이션 와 함께 vector databases 및 semantic search. Use 때 implementing 지식-grounded AI, 구축 document Q&A 시스템, 또는 integrating LLMs 와 함께 외부 지식 기초.
---

# RAG 구현

마스터 검색-Augmented 세대 (RAG) 에 빌드 LLM 애플리케이션 것 provide accurate, grounded 응답 사용하여 외부 지식 sources.

## 때 에 Use This Skill

- 구축 Q&A 시스템 over 독점 문서화합니다
- 생성하는 chatbots 와 함께 현재, factual 정보
- Implementing semantic search 와 함께 natural language 쿼리
- Reducing hallucinations 와 함께 grounded 응답
- 가능하게 하는 LLMs 에 access 도메인-특정 지식
- 구축 문서화 assistants
- 생성하는 research tools 와 함께 소스 citation

## 핵심 컴포넌트

### 1. Vector Databases
**Purpose**: Store 및 retrieve document embeddings efficiently

**Options:**
- **Pinecone**: 관리형, scalable, fast 쿼리
- **Weaviate**: 오픈 소스, 하이브리드 search
- **Milvus**: High 성능, 에-전제
- **Chroma**: 경량, 쉬운 에 use
- **Qdrant**: Fast, 필터링된 search
- **FAISS**: Meta's 라이브러리, 로컬 배포

### 2. Embeddings
**Purpose**: Convert text 에 numerical vectors 위한 similarity search

**모델:**
- **text-embedding-ada-002** (OpenAI): 일반 purpose, 1536 dims
- **모든-MiniLM-L6-v2** (Sentence Transformers): Fast, 경량
- **e5-large-v2**: High 품질, multilingual
- **강사**: 작업-특정 지시사항
- **bge-large-en-v1.5**: SOTA 성능

### 3. 검색 Strategies
**Approaches:**
- **Dense 검색**: Semantic similarity 를 통해 embeddings
- **Sparse 검색**: Keyword 일치하는 (BM25, TF-IDF)
- **하이브리드 Search**: Combine dense + sparse
- **Multi-쿼리**: Generate 여러 쿼리 variations
- **HyDE**: Generate hypothetical 문서화합니다

### 4. Reranking
**Purpose**: Improve 검색 품질 에 의해 reordering results

**메서드:**
- **Cross-Encoders**: BERT-based reranking
- **Cohere Rerank**: API-based reranking
- **Maximal Marginal Relevance (MMR)**: Diversity + relevance
- **LLM-based**: Use LLM 에 score relevance

## Quick Start

```python
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 1. Load documents
loader = DirectoryLoader('./docs', glob="**/*.txt")
documents = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
chunks = text_splitter.split_documents(documents)

# 3. Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# 4. Create retrieval chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=True
)

# 5. Query
result = qa_chain({"query": "What are the main features?"})
print(result['result'])
print(result['source_documents'])
```

## 고급 RAG 패턴

### 패턴 1: 하이브리드 Search
```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever

# Sparse retriever (BM25)
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 5

# Dense retriever (embeddings)
embedding_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Combine with weights
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, embedding_retriever],
    weights=[0.3, 0.7]
)
```

### 패턴 2: Multi-쿼리 검색
```python
from langchain.retrievers.multi_query import MultiQueryRetriever

# Generate multiple query perspectives
retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=OpenAI()
)

# Single query → multiple variations → combined results
results = retriever.get_relevant_documents("What is the main topic?")
```

### 패턴 3: Contextual 압축
```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever()
)

# Returns only relevant parts of documents
compressed_docs = compression_retriever.get_relevant_documents("query")
```

### 패턴 4: Parent Document Retriever
```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

# Store for parent documents
store = InMemoryStore()

# Small chunks for retrieval, large chunks for context
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)
```

## Document 청킹 Strategies

### Recursive Character Text Splitter
```python
from langchain.text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]  # Try these in order
)
```

### 토큰-Based 분할하는
```python
from langchain.text_splitters import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=512,
    chunk_overlap=50
)
```

### Semantic 청킹
```python
from langchain.text_splitters import SemanticChunker

splitter = SemanticChunker(
    embeddings=OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile"
)
```

### Markdown 헤더 Splitter
```python
from langchain.text_splitters import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
```

## Vector Store Configurations

### Pinecone
```python
import pinecone
from langchain.vectorstores import Pinecone

pinecone.init(api_key="your-api-key", environment="us-west1-gcp")

index = pinecone.Index("your-index-name")

vectorstore = Pinecone(index, embeddings.embed_query, "text")
```

### Weaviate
```python
import weaviate
from langchain.vectorstores import Weaviate

client = weaviate.Client("http://localhost:8080")

vectorstore = Weaviate(client, "Document", "content", embeddings)
```

### Chroma (로컬)
```python
from langchain.vectorstores import Chroma

vectorstore = Chroma(
    collection_name="my_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
```

## 검색 최적화

### 1. 메타데이터 필터링
```python
# Add metadata during indexing
chunks_with_metadata = []
for i, chunk in enumerate(chunks):
    chunk.metadata = {
        "source": chunk.metadata.get("source"),
        "page": i,
        "category": determine_category(chunk.page_content)
    }
    chunks_with_metadata.append(chunk)

# Filter during retrieval
results = vectorstore.similarity_search(
    "query",
    filter={"category": "technical"},
    k=5
)
```

### 2. Maximal Marginal Relevance
```python
# Balance relevance with diversity
results = vectorstore.max_marginal_relevance_search(
    "query",
    k=5,
    fetch_k=20,  # Fetch 20, return top 5 diverse
    lambda_mult=0.5  # 0=max diversity, 1=max relevance
)
```

### 3. Reranking 와 함께 Cross-Encoder
```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Get initial results
candidates = vectorstore.similarity_search("query", k=20)

# Rerank
pairs = [[query, doc.page_content] for doc in candidates]
scores = reranker.predict(pairs)

# Sort by score and take top k
reranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)[:5]
```

## Prompt Engineering 위한 RAG

### Contextual Prompt
```python
prompt_template = """Use the following context to answer the question. If you cannot answer based on the context, say "I don't have enough information."

Context:
{context}

Question: {question}

Answer:"""
```

### 와 함께 Citations
```python
prompt_template = """Answer the question based on the context below. Include citations using [1], [2], etc.

Context:
{context}

Question: {question}

Answer (with citations):"""
```

### 와 함께 Confidence
```python
prompt_template = """Answer the question using the context. Provide a confidence score (0-100%) for your answer.

Context:
{context}

Question: {question}

Answer:
Confidence:"""
```

## 평가 메트릭

```python
def evaluate_rag_system(qa_chain, test_cases):
    metrics = {
        'accuracy': [],
        'retrieval_quality': [],
        'groundedness': []
    }

    for test in test_cases:
        result = qa_chain({"query": test['question']})

        # Check if answer matches expected
        accuracy = calculate_accuracy(result['result'], test['expected'])
        metrics['accuracy'].append(accuracy)

        # Check if relevant docs were retrieved
        retrieval_quality = evaluate_retrieved_docs(
            result['source_documents'],
            test['relevant_docs']
        )
        metrics['retrieval_quality'].append(retrieval_quality)

        # Check if answer is grounded in context
        groundedness = check_groundedness(
            result['result'],
            result['source_documents']
        )
        metrics['groundedness'].append(groundedness)

    return {k: sum(v)/len(v) for k, v in metrics.items()}
```

## 리소스

- **참조/vector-databases.md**: 상세한 비교 of vector DBs
- **참조/embeddings.md**: Embedding 모델 선택 가이드
- **참조/검색-strategies.md**: 고급 검색 techniques
- **참조/reranking.md**: Reranking 메서드 및 때 에 use them
- **참조/컨텍스트-window.md**: Managing 컨텍스트 제한합니다
- **자산/vector-store-config.yaml**: 구성 템플릿
- **자산/retriever-파이프라인.py**: 완전한 RAG 파이프라인
- **자산/embedding-모델.md**: 모델 비교 및 benchmarks

## 최선의 관행

1. **Chunk Size**: Balance 사이 컨텍스트 및 specificity (500-1000 토큰)
2. **Overlap**: Use 10-20% overlap 에 preserve 컨텍스트 에서 boundaries
3. **메타데이터**: Include 소스, 페이지, 타임스탬프 위한 필터링 및 디버깅
4. **하이브리드 Search**: Combine semantic 및 keyword search 위한 최선의 results
5. **Reranking**: Improve top results 와 함께 cross-encoder
6. **Citations**: 항상 반환 소스 문서화합니다 위한 transparency
7. **평가**: 지속적으로 test 검색 품질 및 answer 정확성
8. **모니터링**: Track 검색 메트릭 에서 production

## 일반적인 이슈

- **Poor 검색**: Check embedding 품질, chunk size, 쿼리 formulation
- **Irrelevant Results**: Add 메타데이터 필터링, use 하이브리드 search, rerank
- **Missing 정보**: Ensure 문서화합니다 are 적절하게 색인된
- **Slow 쿼리**: Optimize vector store, use 캐싱, reduce k
- **Hallucinations**: Improve grounding prompt, add 확인 단계
