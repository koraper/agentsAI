---
name: grafana-dashboards
description: Create 및 manage production Grafana 대시보드 위한 real-시간 시각화 of 시스템 및 애플리케이션 메트릭. Use 때 구축 모니터링 대시보드, visualizing 메트릭, 또는 생성하는 operational observability 인터페이스.
---

# Grafana 대시보드

Create 및 manage 프로덕션 준비 완료 Grafana 대시보드 위한 포괄적인 시스템 observability.

## Purpose

설계 effective Grafana 대시보드 위한 모니터링 애플리케이션, 인프라, 및 비즈니스 메트릭.

## 때 에 Use

- Visualize Prometheus 메트릭
- Create 사용자 정의 대시보드
- Implement SLO 대시보드
- 모니터 인프라
- Track 비즈니스 KPIs

## 대시보드 설계 원칙

### 1. 계층 of 정보
```
┌─────────────────────────────────────┐
│  Critical Metrics (Big Numbers)     │
├─────────────────────────────────────┤
│  Key Trends (Time Series)           │
├─────────────────────────────────────┤
│  Detailed Metrics (Tables/Heatmaps) │
└─────────────────────────────────────┘
```

### 2. RED 메서드 (서비스)
- **Rate** - 요청 per second
- **오류** - 오류 rate
- **기간** - 지연 시간/응답 시간

### 3. USE 메서드 (리소스)
- **사용률** - % 시간 리소스 is busy
- **포화** - 큐 length/wait 시간
- **오류** - 오류 개수

## 대시보드 구조

### API 모니터링 대시보드

```json
{
  "dashboard": {
    "title": "API Monitoring",
    "tags": ["api", "production"],
    "timezone": "browser",
    "refresh": "30s",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{service}}"
          }
        ],
        "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8}
      },
      {
        "title": "Error Rate %",
        "type": "graph",
        "targets": [
          {
            "expr": "(sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))) * 100",
            "legendFormat": "Error Rate"
          }
        ],
        "alert": {
          "conditions": [
            {
              "evaluator": {"params": [5], "type": "gt"},
              "operator": {"type": "and"},
              "query": {"params": ["A", "5m", "now"]},
              "type": "query"
            }
          ]
        },
        "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8}
      },
      {
        "title": "P95 Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))",
            "legendFormat": "{{service}}"
          }
        ],
        "gridPos": {"x": 0, "y": 8, "w": 24, "h": 8}
      }
    ]
  }
}
```

**참조:** See `assets/api-dashboard.json`

## Panel 유형

### 1. Stat Panel (Single 값)
```json
{
  "type": "stat",
  "title": "Total Requests",
  "targets": [{
    "expr": "sum(http_requests_total)"
  }],
  "options": {
    "reduceOptions": {
      "values": false,
      "calcs": ["lastNotNull"]
    },
    "orientation": "auto",
    "textMode": "auto",
    "colorMode": "value"
  },
  "fieldConfig": {
    "defaults": {
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"value": 0, "color": "green"},
          {"value": 80, "color": "yellow"},
          {"value": 90, "color": "red"}
        ]
      }
    }
  }
}
```

### 2. 시간 시리즈 그래프
```json
{
  "type": "graph",
  "title": "CPU Usage",
  "targets": [{
    "expr": "100 - (avg by (instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
  }],
  "yaxes": [
    {"format": "percent", "max": 100, "min": 0},
    {"format": "short"}
  ]
}
```

### 3. 테이블 Panel
```json
{
  "type": "table",
  "title": "Service Status",
  "targets": [{
    "expr": "up",
    "format": "table",
    "instant": true
  }],
  "transformations": [
    {
      "id": "organize",
      "options": {
        "excludeByName": {"Time": true},
        "indexByName": {},
        "renameByName": {
          "instance": "Instance",
          "job": "Service",
          "Value": "Status"
        }
      }
    }
  ]
}
```

### 4. Heatmap
```json
{
  "type": "heatmap",
  "title": "Latency Heatmap",
  "targets": [{
    "expr": "sum(rate(http_request_duration_seconds_bucket[5m])) by (le)",
    "format": "heatmap"
  }],
  "dataFormat": "tsbuckets",
  "yAxis": {
    "format": "s"
  }
}
```

## 변수

### 쿼리 변수
```json
{
  "templating": {
    "list": [
      {
        "name": "namespace",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(kube_pod_info, namespace)",
        "refresh": 1,
        "multi": false
      },
      {
        "name": "service",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(kube_service_info{namespace=\"$namespace\"}, service)",
        "refresh": 1,
        "multi": true
      }
    ]
  }
}
```

### Use 변수 에서 쿼리
```
sum(rate(http_requests_total{namespace="$namespace", service=~"$service"}[5m]))
```

## 경고 에서 대시보드

```json
{
  "alert": {
    "name": "High Error Rate",
    "conditions": [
      {
        "evaluator": {
          "params": [5],
          "type": "gt"
        },
        "operator": {"type": "and"},
        "query": {
          "params": ["A", "5m", "now"]
        },
        "reducer": {"type": "avg"},
        "type": "query"
      }
    ],
    "executionErrorState": "alerting",
    "for": "5m",
    "frequency": "1m",
    "message": "Error rate is above 5%",
    "noDataState": "no_data",
    "notifications": [
      {"uid": "slack-channel"}
    ]
  }
}
```

## 대시보드 Provisioning

**대시보드.yml:**
```yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: 'General'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/dashboards
```

## 일반적인 대시보드 패턴

### 인프라 대시보드

**키 Panels:**
- CPU 사용률 per 노드
- 메모리 usage per 노드
- 디스크 I/O
- 네트워크 traffic
- Pod 개수 에 의해 namespace
- 노드 상태

**참조:** See `assets/infrastructure-dashboard.json`

### 데이터베이스 대시보드

**키 Panels:**
- 쿼리 per second
- 연결 풀 usage
- 쿼리 지연 시간 (P50, P95, P99)
- 활성 연결
- 데이터베이스 size
- 복제 lag
- Slow 쿼리

**참조:** See `assets/database-dashboard.json`

### 애플리케이션 대시보드

**키 Panels:**
- 요청 rate
- 오류 rate
- 응답 시간 (percentiles)
- 활성 사용자/세션
- 캐시 hit rate
- 큐 length

## 최선의 관행

1. **Start 와 함께 템플릿** (Grafana 커뮤니티 대시보드)
2. **Use 일관된 naming** 위한 panels 및 변수
3. **그룹 관련됨 메트릭** 에서 행
4. **세트 적절한 시간 ranges** (default: 마지막 6 hours)
5. **Use 변수** 위한 flexibility
6. **Add panel descriptions** 위한 컨텍스트
7. **Configure units** 올바르게
8. **세트 의미 있는 thresholds** 위한 colors
9. **Use 일관된 colors** 전반에 걸쳐 대시보드
10. **Test 와 함께 다른 시간 ranges**

## 대시보드 처럼 코드

### Terraform Provisioning

```hcl
resource "grafana_dashboard" "api_monitoring" {
  config_json = file("${path.module}/dashboards/api-monitoring.json")
  folder      = grafana_folder.monitoring.id
}

resource "grafana_folder" "monitoring" {
  title = "Production Monitoring"
}
```

### Ansible Provisioning

```yaml
- name: Deploy Grafana dashboards
  copy:
    src: "{{ item }}"
    dest: /etc/grafana/dashboards/
  with_fileglob:
    - "dashboards/*.json"
  notify: restart grafana
```

## 참조 파일

- `assets/api-dashboard.json` - API 모니터링 대시보드
- `assets/infrastructure-dashboard.json` - 인프라 대시보드
- `assets/database-dashboard.json` - 데이터베이스 모니터링 대시보드
- `references/dashboard-design.md` - 대시보드 설계 가이드

## 관련됨 Skills

- `prometheus-configuration` - 위한 metric 컬렉션
- `slo-implementation` - 위한 SLO 대시보드
