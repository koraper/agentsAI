# API 설계 Checklist

## Pre-구현 Review

### 리소스 설계
- [ ] 리소스 are nouns, not verbs
- [ ] Plural names 위한 collections
- [ ] 일관된 naming 전반에 걸쳐 모든 엔드포인트
- [ ] 명확한 리소스 계층 (avoid deep nesting >2 levels)
- [ ] 모든 CRUD 작업 적절하게 mapped 에 HTTP 메서드

### HTTP 메서드
- [ ] GET 위한 검색 (safe, idempotent)
- [ ] POST 위한 생성
- [ ] PUT 위한 전체 replacement (idempotent)
- [ ] PATCH 위한 부분 업데이트합니다
- [ ] DELETE 위한 removal (idempotent)

### 상태 Codes
- [ ] 200 OK 위한 성공한 GET/PATCH/PUT
- [ ] 201 생성된 위한 POST
- [ ] 204 아니요 콘텐츠 위한 DELETE
- [ ] 400 나쁜 요청 위한 malformed 요청
- [ ] 401 Unauthorized 위한 missing auth
- [ ] 403 금지된 위한 불충분한 권한
- [ ] 404 Not 찾은 위한 missing 리소스
- [ ] 422 Unprocessable 엔터티 위한 검증 오류
- [ ] 429 또한 많은 요청 위한 속도 제한
- [ ] 500 내부 서버 오류 위한 서버 이슈

### Pagination
- [ ] 모든 컬렉션 엔드포인트 paginated
- [ ] default 페이지 size 정의된 (e.g., 20)
- [ ] Maximum 페이지 size 시행됨 (e.g., 100)
- [ ] Pagination 메타데이터 포함된 (총계, 페이지, etc.)
- [ ] Cursor-based 또는 오프셋-based 패턴 선택된

### 필터링 & 정렬
- [ ] 쿼리 매개변수 위한 필터링
- [ ] Sort 매개변수 지원된
- [ ] Search 매개변수 위한 전체-text search
- [ ] 분야 선택 지원된 (sparse fieldsets)

### Versioning
- [ ] Versioning 전략 정의된 (URL/헤더/쿼리)
- [ ] 버전 포함된 에서 모든 엔드포인트
- [ ] Deprecation 정책 문서화된

### 오류 처리
- [ ] 일관된 오류 응답 format
- [ ] 상세한 오류 메시지
- [ ] 분야-레벨 검증 오류
- [ ] 오류 codes 위한 클라이언트 처리
- [ ] Timestamps 에서 오류 응답

### 인증 & 인가
- [ ] 인증 메서드 정의된 (Bearer 토큰, API 키)
- [ ] 인가 확인합니다 에 모든 엔드포인트
- [ ] 401 vs 403 used 올바르게
- [ ] 토큰 expiration 처리된

### 속도 제한
- [ ] Rate 제한합니다 정의된 per 엔드포인트/사용자
- [ ] Rate limit 헤더 포함된
- [ ] 429 상태 코드 위한 exceeded 제한합니다
- [ ] 재시도-이후 헤더 제공된

### 문서화
- [ ] OpenAPI/Swagger spec 생성된
- [ ] 모든 엔드포인트 문서화된
- [ ] 요청/응답 예제 제공된
- [ ] 오류 응답 문서화된
- [ ] 인증 흐름 문서화된

### 테스트
- [ ] 단위 테스트합니다 위한 비즈니스 logic
- [ ] 통합 테스트합니다 위한 엔드포인트
- [ ] 오류 scenarios 테스트된
- [ ] 엣지 cases covered
- [ ] 성능 테스트합니다 위한 heavy 엔드포인트

### Security
- [ ] 입력 검증 에 모든 필드
- [ ] SQL 인젝션 방지
- [ ] XSS 방지
- [ ] CORS 구성된 올바르게
- [ ] HTTPS 시행됨
- [ ] Sensitive 데이터 not 에서 URLs
- [ ] 아니요 secrets 에서 응답

### 성능
- [ ] 데이터베이스 쿼리 최적화된
- [ ] N+1 쿼리 방지된
- [ ] 캐싱 전략 정의된
- [ ] 캐시 헤더 세트 적절하게
- [ ] Large 응답 paginated

### 모니터링
- [ ] 로깅 구현된
- [ ] 오류 추적 구성된
- [ ] 성능 메트릭 수집된
- [ ] Health check 엔드포인트 사용 가능한
- [ ] 경고 구성된 위한 오류

## GraphQL-특정 확인합니다

### 스키마 설계
- [ ] 스키마 우선 접근법 used
- [ ] 유형 적절하게 정의된
- [ ] Non-null vs nullable 결정된
- [ ] 인터페이스/unions used 적절하게
- [ ] 사용자 정의 scalars 정의된

### 쿼리
- [ ] 쿼리 depth 제한하는
- [ ] 쿼리 complexity 분석
- [ ] DataLoaders prevent N+1
- [ ] Pagination 패턴 선택된 (Relay/오프셋)

### Mutations
- [ ] 입력 유형 정의된
- [ ] 페이로드 유형 와 함께 오류
- [ ] Optimistic 응답 지원
- [ ] Idempotency considered

### 성능
- [ ] DataLoader 위한 모든 관계
- [ ] 쿼리 배치 활성화됨
- [ ] 유지된 쿼리 considered
- [ ] 응답 캐싱 구현된

### 문서화
- [ ] 모든 필드 문서화된
- [ ] Deprecations 표시된
- [ ] 예제 제공된
- [ ] 스키마 introspection 활성화됨
