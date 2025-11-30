# Multi-플랫폼 기능 개발 워크플로우

빌드 및 deploy the same 기능 consistently 전반에 걸쳐 web, mobile, 및 desktop 플랫폼 사용하여 API-첫 번째 아키텍처 및 병렬로 구현 strategies.

[확장된 thinking: This 워크플로우 오케스트레이션합니다 여러 specialized 에이전트 에 ensure 기능 parity 전반에 걸쳐 플랫폼 동안 maintaining 플랫폼-특정 optimizations. The 조정 전략 강조합니다 shared 계약 및 병렬로 개발 와 함께 일반 동기화 points. 에 의해 establishing API 계약 및 데이터 모델 upfront, teams can work independently 동안 보장하는 일관성. The 워크플로우 benefits include faster 시간-에-market, 감소된 통합 이슈, 및 maintainable 크로스 플랫폼 codebases.]

## 단계 1: 아키텍처 및 API 설계 (Sequential)

### 1. Define 기능 요구사항 및 API 계약
- Use 작업 tool 와 함께 subagent_type="backend-아키텍트"
- Prompt: "설계 the API 계약 위한 기능: $인수. Create OpenAPI 3.1 사양 와 함께:
  - RESTful 엔드포인트 와 함께 적절한 HTTP 메서드 및 상태 codes
  - GraphQL 스키마 만약 적용 가능한 위한 복잡한 데이터 쿼리
  - WebSocket 이벤트 위한 real-시간 기능
  - 요청/응답 스키마 와 함께 검증 규칙
  - 인증 및 인가 요구사항
  - 속도 제한 및 캐싱 strategies
  - 오류 응답 형식을 지정합니다 및 codes
  Define shared 데이터 모델 것 모든 플랫폼 will consume."
- 예상되는 출력: 완전한 API 사양, 데이터 모델, 및 통합 가이드라인

### 2. 설계 시스템 및 UI/UX 일관성
- Use 작업 tool 와 함께 subagent_type="ui-ux-디자이너"
- Prompt: "Create 크로스 플랫폼 설계 시스템 위한 기능 사용하여 API spec: [이전 출력]. Include:
  - 컴포넌트 사양 위한 각 플랫폼 (Material 설계, iOS HIG, Fluent)
  - Responsive 레이아웃 위한 web (모바일 우선 접근법)
  - Native 패턴 위한 iOS (SwiftUI) 및 Android (Material You)
  - Desktop-특정 considerations (keyboard shortcuts, window 관리)
  - 접근성 요구사항 (WCAG 2.2 레벨 AA)
  - Dark/light theme 사양
  - Animation 및 transition 가이드라인"
- 컨텍스트 에서 이전: API 엔드포인트, 데이터 구조, 인증 흐릅니다
- 예상되는 출력: 설계 시스템 문서화, 컴포넌트 라이브러리 specs, 플랫폼 가이드라인

### 3. Shared 비즈니스 Logic 아키텍처
- Use 작업 tool 와 함께 subagent_type="포괄적인-review::아키텍트-review"
- Prompt: "설계 shared 비즈니스 logic 아키텍처 위한 크로스 플랫폼 기능. Define:
  - 핵심 도메인 모델 및 엔터티 (플랫폼 독립적)
  - 비즈니스 규칙 및 검증 logic
  - 상태 관리 패턴 (MVI/Redux/BLoC)
  - 캐싱 및 offline strategies
  - 오류 처리 및 재시도 정책
  - 플랫폼-특정 어댑터 패턴
  Consider Kotlin Multiplatform 위한 mobile 또는 TypeScript 위한 web/desktop sharing."
- 컨텍스트 에서 이전: API 계약, 데이터 모델, UI 요구사항
- 예상되는 출력: Shared 코드 아키텍처, 플랫폼 추상화 layers, 구현 가이드

## 단계 2: 병렬로 플랫폼 구현

### 4a. Web 구현 (React/다음.js)
- Use 작업 tool 와 함께 subagent_type="frontend-개발자"
- Prompt: "Implement web 버전 of 기능 사용하여:
  - React 18+ 와 함께 다음.js 14+ App 라우터
  - TypeScript 위한 유형 safety
  - TanStack 쿼리 위한 API 통합: [API spec]
  - Zustand/Redux Toolkit 위한 상태 관리
  - Tailwind CSS 와 함께 설계 시스템: [설계 specs]
  - Progressive Web App 역량
  - SSR/SSG 최적화 곳 적절한
  - Web vitals 최적화 (LCP < 2.5s, FID < 100ms)
  Follow shared 비즈니스 logic: [아키텍처 doc]"
- 컨텍스트 에서 이전: API 계약, 설계 시스템, shared logic 패턴
- 예상되는 출력: 완전한 web 구현 와 함께 테스트합니다

### 4b. iOS 구현 (SwiftUI)
- Use 작업 tool 와 함께 subagent_type="ios-개발자"
- Prompt: "Implement iOS 버전 사용하여:
  - SwiftUI 와 함께 iOS 17+ 기능
  - Swift 5.9+ 와 함께 비동기/await
  - URLSession 와 함께 Combine 위한 API: [API spec]
  - 핵심 데이터/SwiftData 위한 지속성
  - 설계 시스템 compliance: [iOS HIG specs]
  - Widget extensions 만약 적용 가능한
  - 플랫폼-특정 기능 (Face ID, Haptics, Live Activities)
  - Testable MVVM 아키텍처
  Follow shared 패턴: [아키텍처 doc]"
- 컨텍스트 에서 이전: API 계약, iOS 설계 가이드라인, shared 모델
- 예상되는 출력: Native iOS 구현 와 함께 단위/UI 테스트합니다

### 4c. Android 구현 (Kotlin/Compose)
- Use 작업 tool 와 함께 subagent_type="mobile-개발자"
- Prompt: "Implement Android 버전 사용하여:
  - Jetpack Compose 와 함께 Material 3
  - Kotlin coroutines 및 흐름
  - Retrofit/Ktor 위한 API: [API spec]
  - Room 데이터베이스 위한 로컬 스토리지
  - Hilt 위한 종속성 인젝션
  - Material You 동적 테마 지정: [설계 specs]
  - 플랫폼 기능 (biometric auth, widgets)
  - Clean 아키텍처 와 함께 MVI 패턴
  Follow shared logic: [아키텍처 doc]"
- 컨텍스트 에서 이전: API 계약, Material 설계 specs, shared 패턴
- 예상되는 출력: Native Android 구현 와 함께 테스트합니다

### 4d. Desktop 구현 (선택적 - Electron/Tauri)
- Use 작업 tool 와 함께 subagent_type="frontend-mobile-개발::frontend-개발자"
- Prompt: "Implement desktop 버전 사용하여 Tauri 2.0 또는 Electron 와 함께:
  - Shared web codebase 곳 possible
  - Native OS 통합 (시스템 tray, 알림)
  - 파일 시스템 access 만약 필요한
  - Auto-updater 기능
  - 코드 서명 및 notarization 설정
  - Keyboard shortcuts 및 menu bar
  - Multi-window 지원 만약 적용 가능한
  Reuse web 컴포넌트: [web 구현]"
- 컨텍스트 에서 이전: Web 구현, desktop-특정 요구사항
- 예상되는 출력: Desktop 애플리케이션 와 함께 플랫폼 패키지

## 단계 3: 통합 및 검증

### 5. API 문서화 및 테스트
- Use 작업 tool 와 함께 subagent_type="문서화-세대::api-documenter"
- Prompt: "Create 포괄적인 API 문서화 포함하여:
  - Interactive OpenAPI/Swagger 문서화
  - 플랫폼-특정 통합 안내합니다
  - SDK 예제 위한 각 플랫폼
  - 인증 흐름 다이어그램
  - 속도 제한 및 quota 정보
  - Postman/Insomnia collections
  - WebSocket 연결 예제
  - 오류 처리 최선의 관행
  - API versioning 전략
  Test 모든 엔드포인트 와 함께 플랫폼 implementations."
- 컨텍스트 에서 이전: 구현된 플랫폼, API usage 패턴
- 예상되는 출력: 완전한 API 문서화 portal, test results

### 6. 크로스 플랫폼 테스트 및 기능 Parity
- Use 작업 tool 와 함께 subagent_type="단위-테스트::test-automator"
- Prompt: "Validate 기능 parity 전반에 걸쳐 모든 플랫폼:
  - 기능적인 테스트 매트릭스 (기능 work identically)
  - UI 일관성 확인 (따릅니다 설계 시스템)
  - 성능 benchmarks per 플랫폼
  - 접근성 테스트 (플랫폼-특정 tools)
  - 네트워크 복원력 테스트 (offline, slow 연결)
  - 데이터 동기화 검증
  - 플랫폼-특정 엣지 cases
  - End-에-최종 사용자 journey 테스트합니다
  Create test 보고서 와 함께 어떤 플랫폼 discrepancies."
- 컨텍스트 에서 이전: 모든 플랫폼 implementations, API 문서화
- 예상되는 출력: Test 보고서, parity 매트릭스, 성능 메트릭

### 7. 플랫폼-특정 Optimizations
- Use 작업 tool 와 함께 subagent_type="애플리케이션-성능::성능-엔지니어"
- Prompt: "Optimize 각 플랫폼 구현:
  - Web: Bundle size, lazy 로드, CDN 설정, SEO
  - iOS: App size, launch 시간, 메모리 usage, battery
  - Android: APK size, startup 시간, frame rate, battery
  - Desktop: 바이너리 size, 리소스 usage, startup 시간
  - API: 응답 시간, 캐싱, 압축
  Maintain 기능 parity 동안 leveraging 플랫폼 strengths.
  Document 최적화 techniques 및 trade-offs."
- 컨텍스트 에서 이전: Test results, 성능 메트릭
- 예상되는 출력: 최적화된 implementations, 성능 improvements

## 구성 Options

- **--플랫폼**: Specify target 플랫폼 (web,ios,android,desktop)
- **--api-첫 번째**: Generate API 이전 UI 구현 (default: 참)
- **--shared-코드**: Use Kotlin Multiplatform 또는 similar (default: evaluate)
- **--설계-시스템**: Use 기존 또는 create 새로운 (default: create)
- **--테스트-전략**: 단위, 통합, e2e (default: 모든)

## Success Criteria

- API 계약 정의된 및 검증된 이전 구현
- 모든 플랫폼 achieve 기능 parity 와 함께 <5% 분산
- 성능 메트릭 meet 플랫폼-특정 표준
- 접근성 표준 met (WCAG 2.2 AA minimum)
- 크로스 플랫폼 테스트 표시합니다 일관된 behavior
- 문서화 완전한 위한 모든 플랫폼
- 코드 reuse >40% 사이 플랫폼 곳 적용 가능한
- 사용자 experience 최적화된 위한 각 플랫폼's 규약

## 플랫폼-특정 Considerations

**Web**: PWA 역량, SEO 최적화, browser compatibility
**iOS**: App Store 가이드라인, TestFlight 배포, iOS-특정 기능
**Android**: Play Store 요구사항, Android App 번들링합니다, device 단편화
**Desktop**: 코드 서명, auto-업데이트합니다, OS-특정 installers

초기 기능 사양: $인수