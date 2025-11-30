---
name: slo-implementation
description: Define 및 implement 서비스 레벨 Indicators (SLIs) 및 서비스 레벨 Objectives (SLOs) 와 함께 오류 budgets 및 경고. Use 때 establishing 신뢰성 targets, implementing SRE 관행, 또는 measuring 서비스 성능.
---

# SLO 구현

프레임워크 위한 defining 및 implementing 서비스 레벨 Indicators (SLIs), 서비스 레벨 Objectives (SLOs), 및 오류 budgets.

## Purpose

Implement measurable 신뢰성 targets 사용하여 SLIs, SLOs, 및 오류 budgets 에 balance 신뢰성 와 함께 innovation velocity.

## 때 에 Use

- Define 서비스 신뢰성 targets
- 측정 사용자-perceived 신뢰성
- Implement 오류 budgets
- Create SLO-based 경고
- Track 신뢰성 goals

## SLI/SLO/SLA 계층

```
SLA (Service Level Agreement)
  ↓ Contract with customers
SLO (Service Level Objective)
  ↓ Internal reliability target
SLI (Service Level Indicator)
  ↓ Actual measurement
```

## Defining SLIs

### 일반적인 SLI 유형

#### 1. 가용성 SLI
```promql
# Successful requests / Total requests
sum(rate(http_requests_total{status!~"5.."}[28d]))
/
sum(rate(http_requests_total[28d]))
```

#### 2. 지연 시간 SLI
```promql
# Requests below latency threshold / Total requests
sum(rate(http_request_duration_seconds_bucket{le="0.5"}[28d]))
/
sum(rate(http_request_duration_seconds_count[28d]))
```

#### 3. 내구성 SLI
```
# Successful writes / Total writes
sum(storage_writes_successful_total)
/
sum(storage_writes_total)
```

**참조:** See `references/slo-definitions.md`

## Setting SLO Targets

### 가용성 SLO 예제

| SLO % | Downtime/Month | Downtime/Year |
|-------|----------------|---------------|
| 99%   | 7.2 hours      | 3.65 days     |
| 99.9% | 43.2 minutes   | 8.76 hours    |
| 99.95%| 21.6 minutes   | 4.38 hours    |
| 99.99%| 4.32 minutes   | 52.56 minutes |

### Choose 적절한 SLOs

**Consider:**
- 사용자 expectations
- 비즈니스 요구사항
- 현재 성능
- Cost of 신뢰성
- Competitor benchmarks

**예제 SLOs:**
```yaml
slos:
  - name: api_availability
    target: 99.9
    window: 28d
    sli: |
      sum(rate(http_requests_total{status!~"5.."}[28d]))
      /
      sum(rate(http_requests_total[28d]))

  - name: api_latency_p95
    target: 99
    window: 28d
    sli: |
      sum(rate(http_request_duration_seconds_bucket{le="0.5"}[28d]))
      /
      sum(rate(http_request_duration_seconds_count[28d]))
```

## 오류 Budget 계산

### 오류 Budget 공식

```
Error Budget = 1 - SLO Target
```

**예제:**
- SLO: 99.9% 가용성
- 오류 Budget: 0.1% = 43.2 minutes/month
- 현재 오류: 0.05% = 21.6 minutes/month
- Remaining Budget: 50%

### 오류 Budget 정책

```yaml
error_budget_policy:
  - remaining_budget: 100%
    action: Normal development velocity
  - remaining_budget: 50%
    action: Consider postponing risky changes
  - remaining_budget: 10%
    action: Freeze non-critical changes
  - remaining_budget: 0%
    action: Feature freeze, focus on reliability
```

**참조:** See `references/error-budget.md`

## SLO 구현

### Prometheus 기록 규칙

```yaml
# SLI Recording Rules
groups:
  - name: sli_rules
    interval: 30s
    rules:
      # Availability SLI
      - record: sli:http_availability:ratio
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[28d]))
          /
          sum(rate(http_requests_total[28d]))

      # Latency SLI (requests < 500ms)
      - record: sli:http_latency:ratio
        expr: |
          sum(rate(http_request_duration_seconds_bucket{le="0.5"}[28d]))
          /
          sum(rate(http_request_duration_seconds_count[28d]))

  - name: slo_rules
    interval: 5m
    rules:
      # SLO compliance (1 = meeting SLO, 0 = violating)
      - record: slo:http_availability:compliance
        expr: sli:http_availability:ratio >= bool 0.999

      - record: slo:http_latency:compliance
        expr: sli:http_latency:ratio >= bool 0.99

      # Error budget remaining (percentage)
      - record: slo:http_availability:error_budget_remaining
        expr: |
          (sli:http_availability:ratio - 0.999) / (1 - 0.999) * 100

      # Error budget burn rate
      - record: slo:http_availability:burn_rate_5m
        expr: |
          (1 - (
            sum(rate(http_requests_total{status!~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          )) / (1 - 0.999)
```

### SLO 경고 규칙

```yaml
groups:
  - name: slo_alerts
    interval: 1m
    rules:
      # Fast burn: 14.4x rate, 1 hour window
      # Consumes 2% error budget in 1 hour
      - alert: SLOErrorBudgetBurnFast
        expr: |
          slo:http_availability:burn_rate_1h > 14.4
          and
          slo:http_availability:burn_rate_5m > 14.4
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Fast error budget burn detected"
          description: "Error budget burning at {{ $value }}x rate"

      # Slow burn: 6x rate, 6 hour window
      # Consumes 5% error budget in 6 hours
      - alert: SLOErrorBudgetBurnSlow
        expr: |
          slo:http_availability:burn_rate_6h > 6
          and
          slo:http_availability:burn_rate_30m > 6
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Slow error budget burn detected"
          description: "Error budget burning at {{ $value }}x rate"

      # Error budget exhausted
      - alert: SLOErrorBudgetExhausted
        expr: slo:http_availability:error_budget_remaining < 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "SLO error budget exhausted"
          description: "Error budget remaining: {{ $value }}%"
```

## SLO 대시보드

**Grafana 대시보드 구조:**

```
┌────────────────────────────────────┐
│ SLO Compliance (Current)           │
│ ✓ 99.95% (Target: 99.9%)          │
├────────────────────────────────────┤
│ Error Budget Remaining: 65%        │
│ ████████░░ 65%                     │
├────────────────────────────────────┤
│ SLI Trend (28 days)                │
│ [Time series graph]                │
├────────────────────────────────────┤
│ Burn Rate Analysis                 │
│ [Burn rate by time window]         │
└────────────────────────────────────┘
```

**예제 쿼리:**

```promql
# Current SLO compliance
sli:http_availability:ratio * 100

# Error budget remaining
slo:http_availability:error_budget_remaining

# Days until error budget exhausted (at current burn rate)
(slo:http_availability:error_budget_remaining / 100)
*
28
/
(1 - sli:http_availability:ratio) * (1 - 0.999)
```

## Multi-Window Burn Rate 경고

```yaml
# Combination of short and long windows reduces false positives
rules:
  - alert: SLOBurnRateHigh
    expr: |
      (
        slo:http_availability:burn_rate_1h > 14.4
        and
        slo:http_availability:burn_rate_5m > 14.4
      )
      or
      (
        slo:http_availability:burn_rate_6h > 6
        and
        slo:http_availability:burn_rate_30m > 6
      )
    labels:
      severity: critical
```

## SLO Review 프로세스

### Weekly Review
- 현재 SLO compliance
- 오류 budget 상태
- Trend 분석
- 인시던트 impact

### Monthly Review
- SLO achievement
- 오류 budget usage
- 인시던트 postmortems
- SLO adjustments

### Quarterly Review
- SLO relevance
- Target adjustments
- 프로세스 improvements
- Tooling enhancements

## 최선의 관행

1. **Start 와 함께 사용자-facing 서비스**
2. **Use 여러 SLIs** (가용성, 지연 시간, etc.)
3. **세트 achievable SLOs** (don't aim 위한 100%)
4. **Implement multi-window 경고** 에 reduce noise
5. **Track 오류 budget** consistently
6. **Review SLOs 정기적으로**
7. **Document SLO decisions**
8. **Align 와 함께 비즈니스 goals**
9. **Automate SLO reporting**
10. **Use SLOs 위한 우선순위 지정**

## 참조 파일

- `assets/slo-template.md` - SLO 정의 템플릿
- `references/slo-definitions.md` - SLO 정의 패턴
- `references/error-budget.md` - 오류 budget calculations

## 관련됨 Skills

- `prometheus-configuration` - 위한 metric 컬렉션
- `grafana-dashboards` - 위한 SLO 시각화
