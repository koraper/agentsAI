# 완전한 Git 워크플로우 와 함께 Multi-에이전트 오케스트레이션

Orchestrate a 포괄적인 git 워크플로우 에서 코드 review 통해 PR 생성, leveraging specialized 에이전트 위한 품질 assurance, 테스트, 및 배포 readiness. This 워크플로우 구현합니다 현대적인 git 최선의 관행 포함하여 기존 Commits, 자동화된 테스트, 및 구조화된 PR 생성.

[확장된 thinking: This 워크플로우 조정합니다 여러 specialized 에이전트 에 ensure 코드 품질 이전 commits are made. The 코드-리뷰어 에이전트 수행합니다 초기 품질 확인합니다, test-automator 보장합니다 모든 테스트합니다 pass, 및 배포-엔지니어 확인합니다 production readiness. 에 의해 orchestrating these 에이전트 순차적으로 와 함께 컨텍스트 passing, we prevent 고장난 코드 에서 entering the 저장소 동안 maintaining high velocity. The 워크플로우 지원합니다 둘 다 trunk-based 및 기능-branch strategies 와 함께 구성 가능한 options 위한 다른 팀 needs.]

## 구성

**Target branch**: $인수 (defaults 에 'main' 만약 not 지정된)

**지원된 flags**:
- `--skip-tests`: Skip 자동화된 test 실행 (use 와 함께 caution)
- `--draft-pr`: Create PR 처럼 초안 위한 work-에서-진행
- `--no-push`: Perform 모든 확인합니다 그러나 don't push 에 remote
- `--squash`: Squash commits 이전 pushing
- `--conventional`: Enforce 기존 Commits format strictly
- `--trunk-based`: Use trunk-based 개발 워크플로우
- `--feature-branch`: Use 기능 branch 워크플로우 (default)

## 단계 1: Pre-커밋 Review 및 분석

### 1. 코드 품질 평가
- Use 작업 tool 와 함께 subagent_type="코드-리뷰어"
- Prompt: "Review 모든 uncommitted 변경합니다 위한 코드 품질 이슈. Check 위한: 1) 코드 스타일 위반, 2) Security 취약점, 3) 성능 concerns, 4) Missing 오류 처리, 5) 불완전한 implementations. Generate a 상세한 보고서 와 함께 severity levels (긴급/high/medium/low) 및 provide 특정 line-에 의해-line feedback. 출력 format: JSON 와 함께 {이슈: [], summary: {긴급: 0, high: 0, medium: 0, low: 0}, recommendations: []}"
- 예상되는 출력: 구조화된 코드 review 보고서 위한 다음 단계

### 2. 종속성 및 Breaking 변경 분석
- Use 작업 tool 와 함께 subagent_type="코드-리뷰어"
- Prompt: "Analyze the 변경합니다 위한: 1) 새로운 종속성 또는 버전 변경합니다, 2) Breaking API 변경합니다, 3) 데이터베이스 스키마 modifications, 4) 구성 변경합니다, 5) 뒤로 compatibility 이슈. 컨텍스트 에서 이전 review: [insert 이슈 summary]. Identify 어떤 변경합니다 것 require 마이그레이션 스크립트 또는 문서화 업데이트합니다."
- 컨텍스트 에서 이전: 코드 품질 이슈 것 might indicate breaking 변경합니다
- 예상되는 출력: Breaking 변경 평가 및 마이그레이션 요구사항

## 단계 2: 테스트 및 검증

### 1. Test 실행 및 Coverage
- Use 작업 tool 와 함께 subagent_type="단위-테스트::test-automator"
- Prompt: "Execute 모든 test suites 위한 the 수정된 코드. Run: 1) 단위 테스트합니다, 2) 통합 테스트합니다, 3) End-에-end 테스트합니다 만약 적용 가능한. Generate coverage 보고서 및 identify 어떤 untested 코드 경로. Based 에 review 이슈: [insert 긴급/high 이슈], ensure 테스트합니다 cover the 문제 areas. Provide test results 에서 format: {통과: [], 실패: [], 건너뜀: [], coverage: {statements: %, branches: %, 함수: %, lines: %}, untested_critical_paths: []}"
- 컨텍스트 에서 이전: 긴급 코드 review 이슈 것 need test coverage
- 예상되는 출력: 완전한 test results 및 coverage 메트릭

### 2. Test Recommendations 및 간격 분석
- Use 작업 tool 와 함께 subagent_type="단위-테스트::test-automator"
- Prompt: "Based 에 test results [insert summary] 및 코드 변경합니다, identify: 1) Missing test scenarios, 2) 엣지 cases not covered, 3) 통합 points needing 확인, 4) 성능 benchmarks 필요한. Generate test 구현 recommendations 우선순위가 지정됨 에 의해 위험. Consider the breaking 변경합니다 식별된: [insert breaking 변경합니다]."
- 컨텍스트 에서 이전: Test results, breaking 변경합니다, untested 경로
- 예상되는 출력: 우선순위가 지정됨 목록 of additional 테스트합니다 필요한

## 단계 3: 커밋 메시지 세대

### 1. 변경 분석 및 분류
- Use 작업 tool 와 함께 subagent_type="코드-리뷰어"
- Prompt: "Analyze 모든 변경합니다 및 categorize them according 에 기존 Commits 사양. Identify the primary 변경 유형 (feat/fix/docs/스타일/refactor/perf/test/빌드/ci/chore/revert) 및 범위. 위한 변경합니다: [insert 파일 목록 및 summary], determine 만약 this should be a single 커밋 또는 여러 원자적 commits. Consider test results: [insert test summary]."
- 컨텍스트 에서 이전: Test results, 코드 review summary
- 예상되는 출력: 커밋 구조 권장사항

### 2. 기존 커밋 메시지 생성
- Use 작업 tool 와 함께 subagent_type="llm-애플리케이션-dev::prompt-엔지니어"
- Prompt: "Create 기존 Commits format 메시지(s) based 에 분류: [insert 분류]. Format: <유형>(<범위>): <subject> 와 함께 blank line then <본문> explaining 무엇 및 왜 (not 어떻게), then <푸터> 와 함께 BREAKING 변경: 만약 적용 가능한. Include: 1) 명확한 subject line (50 chars max), 2) 상세한 본문 explaining rationale, 3) 참조 에 이슈/tickets, 4) Co-authors 만약 적용 가능한. Consider the impact: [insert breaking 변경합니다 만약 어떤]."
- 컨텍스트 에서 이전: 변경 분류, breaking 변경합니다
- 예상되는 출력: 적절하게 형식이 지정된 커밋 메시지(s)

## 단계 4: Branch 전략 및 Push 준비

### 1. Branch 관리
- Use 작업 tool 와 함께 subagent_type="cicd-자동화::배포-엔지니어"
- Prompt: "Based 에 워크플로우 유형 [--trunk-based 또는 --기능-branch], prepare branch 전략. 위한 기능 branch: ensure branch name 따릅니다 패턴 (기능|bugfix|hotfix)/<ticket>-<설명>. 위한 trunk-based: prepare 위한 직접 main push 와 함께 기능 flag 전략 만약 필요한. 현재 branch: [insert branch], target: [insert target branch]. Verify 아니요 conflicts 와 함께 target branch."
- 예상되는 출력: Branch 준비 명령 및 conflict 상태

### 2. Pre-Push 검증
- Use 작업 tool 와 함께 subagent_type="cicd-자동화::배포-엔지니어"
- Prompt: "Perform 최종 pre-push 확인합니다: 1) Verify 모든 CI 확인합니다 will pass, 2) Confirm 아니요 sensitive 데이터 에서 commits, 3) Validate 커밋 signatures 만약 필수, 4) Check branch 보호 규칙, 5) Ensure 모든 review comments addressed. Test summary: [insert test results]. Review 상태: [insert review summary]."
- 컨텍스트 에서 이전: 모든 이전 검증 results
- 예상되는 출력: Push readiness confirmation 또는 차단 이슈

## 단계 5: Pull 요청 생성

### 1. PR 설명 세대
- Use 작업 tool 와 함께 subagent_type="문서화-세대::docs-아키텍트"
- Prompt: "Create 포괄적인 PR 설명 포함하여: 1) Summary of 변경합니다 (무엇 및 왜), 2) 유형 of 변경 checklist, 3) 테스트 수행된 summary 에서 [insert test results], 4) Screenshots/recordings 만약 UI 변경합니다, 5) 배포 notes 에서 [insert 배포 considerations], 6) 관련됨 이슈/tickets, 7) Breaking 변경합니다 section 만약 적용 가능한: [insert breaking 변경합니다], 8) 리뷰어 checklist. Format 처럼 GitHub-flavored Markdown."
- 컨텍스트 에서 이전: 모든 검증 results, test outcomes, breaking 변경합니다
- 예상되는 출력: 완전한 PR 설명 에서 Markdown

### 2. PR 메타데이터 및 자동화 설정
- Use 작업 tool 와 함께 subagent_type="cicd-자동화::배포-엔지니어"
- Prompt: "Configure PR 메타데이터: 1) Assign 적절한 reviewers based 에 CODEOWNERS, 2) Add 라벨링합니다 (유형, priority, 컴포넌트), 3) 링크 관련됨 이슈, 4) 세트 milestone 만약 적용 가능한, 5) Configure merge 전략 (squash/merge/rebase), 6) 세트 up auto-merge 만약 모든 확인합니다 pass. Consider 초안 상태: [--초안-pr flag]. Include test 상태: [insert test summary]."
- 컨텍스트 에서 이전: PR 설명, test results, review 상태
- 예상되는 출력: PR 구성 명령 및 자동화 규칙

## Success Criteria

- ✅ 모든 긴급 및 high-severity 코드 이슈 해결된
- ✅ Test coverage 유지됨 또는 개선된 (target: >80%)
- ✅ 모든 테스트합니다 passing (단위, 통합, e2e)
- ✅ 커밋 메시지 follow 기존 Commits format
- ✅ 아니요 merge conflicts 와 함께 target branch
- ✅ PR 설명 완전한 와 함께 모든 필수 sections
- ✅ Branch 보호 규칙 satisfied
- ✅ Security scanning 완료됨 와 함께 아니요 긴급 취약점
- ✅ 성능 benchmarks 내에 acceptable thresholds
- ✅ 문서화 업데이트된 위한 어떤 API 변경합니다

## 롤백 절차

에서 case of 이슈 이후 merge:

1. **Immediate Revert**: Create revert PR 와 함께 `git revert <commit-hash>`
2. **기능 Flag Disable**: 만약 사용하여 기능 flags, disable 즉시
3. **Hotfix Branch**: 위한 긴급 이슈, create hotfix branch 에서 main
4. **Communication**: Notify 팀 를 통해 designated channels
5. **근 Cause 분석**: Document 이슈 에서 postmortem 템플릿

## 최선의 관행 참조

- **커밋 Frequency**: 커밋 early 및 자주, 그러나 ensure 각 커밋 is 원자적
- **Branch Naming**: `(feature|bugfix|hotfix|docs|chore)/<ticket-id>-<brief-description>`
- **PR Size**: Keep PRs under 400 lines 위한 effective review
- **Review 응답**: 주소 review comments 내에 24 hours
- **Merge 전략**: Squash 위한 기능 branches, merge 위한 릴리스 branches
- **Sign-꺼짐**: Require 에서 least 2 approvals 위한 main branch 변경합니다