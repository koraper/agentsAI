---
name: prometheus-configuration
description: 세트 up Prometheus 위한 포괄적인 metric 컬렉션, 스토리지, 및 모니터링 of 인프라 및 애플리케이션. Use 때 implementing 메트릭 컬렉션, 설정하는 모니터링 인프라, 또는 configuring 경고 시스템.
---

# Prometheus 구성

완전한 가이드 에 Prometheus 설정, metric 컬렉션, scrape 구성, 및 기록 규칙.

## Purpose

Configure Prometheus 위한 포괄적인 metric 컬렉션, 경고, 및 모니터링 of 인프라 및 애플리케이션.

## 때 에 Use

- 세트 up Prometheus 모니터링
- Configure metric scraping
- Create 기록 규칙
- 설계 경고 규칙
- Implement 서비스 발견

## Prometheus 아키텍처

```
┌──────────────┐
│ Applications │ ← Instrumented with client libraries
└──────┬───────┘
       │ /metrics endpoint
       ↓
┌──────────────┐
│  Prometheus  │ ← Scrapes metrics periodically
│    Server    │
└──────┬───────┘
       │
       ├─→ AlertManager (alerts)
       ├─→ Grafana (visualization)
       └─→ Long-term storage (Thanos/Cortex)
```

## Installation

### Kubernetes 와 함께 Helm

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageVolumeSize=50Gi
```

### Docker Compose

```yaml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'

volumes:
  prometheus-data:
```

## 구성 파일

**prometheus.yml:**
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    region: 'us-west-2'

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

# Load rules files
rule_files:
  - /etc/prometheus/rules/*.yml

# Scrape configurations
scrape_configs:
  # Prometheus itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node exporters
  - job_name: 'node-exporter'
    static_configs:
      - targets:
        - 'node1:9100'
        - 'node2:9100'
        - 'node3:9100'
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        regex: '([^:]+)(:[0-9]+)?'
        replacement: '${1}'

  # Kubernetes pods with annotations
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: pod

  # Application metrics
  - job_name: 'my-app'
    static_configs:
      - targets:
        - 'app1.example.com:9090'
        - 'app2.example.com:9090'
    metrics_path: '/metrics'
    scheme: 'https'
    tls_config:
      ca_file: /etc/prometheus/ca.crt
      cert_file: /etc/prometheus/client.crt
      key_file: /etc/prometheus/client.key
```

**참조:** See `assets/prometheus.yml.template`

## Scrape Configurations

### 정적 Targets

```yaml
scrape_configs:
  - job_name: 'static-targets'
    static_configs:
      - targets: ['host1:9100', 'host2:9100']
        labels:
          env: 'production'
          region: 'us-west-2'
```

### 파일-based 서비스 발견

```yaml
scrape_configs:
  - job_name: 'file-sd'
    file_sd_configs:
      - files:
        - /etc/prometheus/targets/*.json
        - /etc/prometheus/targets/*.yml
        refresh_interval: 5m
```

**targets/production.json:**
```json
[
  {
    "targets": ["app1:9090", "app2:9090"],
    "labels": {
      "env": "production",
      "service": "api"
    }
  }
]
```

### Kubernetes 서비스 발견

```yaml
scrape_configs:
  - job_name: 'kubernetes-services'
    kubernetes_sd_configs:
      - role: service
    relabel_configs:
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
        action: replace
        target_label: __scheme__
        regex: (https?)
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
```

**참조:** See `references/scrape-configs.md`

## 기록 규칙

Create pre-계산된 메트릭 위한 자주 queried expressions:

```yaml
# /etc/prometheus/rules/recording_rules.yml
groups:
  - name: api_metrics
    interval: 15s
    rules:
      # HTTP request rate per service
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))

      # Error rate percentage
      - record: job:http_requests_errors:rate5m
        expr: sum by (job) (rate(http_requests_total{status=~"5.."}[5m]))

      - record: job:http_requests_error_rate:percentage
        expr: |
          (job:http_requests_errors:rate5m / job:http_requests:rate5m) * 100

      # P95 latency
      - record: job:http_request_duration:p95
        expr: |
          histogram_quantile(0.95,
            sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
          )

  - name: resource_metrics
    interval: 30s
    rules:
      # CPU utilization percentage
      - record: instance:node_cpu:utilization
        expr: |
          100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

      # Memory utilization percentage
      - record: instance:node_memory:utilization
        expr: |
          100 - ((node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100)

      # Disk usage percentage
      - record: instance:node_disk:utilization
        expr: |
          100 - ((node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100)
```

**참조:** See `references/recording-rules.md`

## 경고 규칙

```yaml
# /etc/prometheus/rules/alert_rules.yml
groups:
  - name: availability
    interval: 30s
    rules:
      - alert: ServiceDown
        expr: up{job="my-app"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.instance }} is down"
          description: "{{ $labels.job }} has been down for more than 1 minute"

      - alert: HighErrorRate
        expr: job:http_requests_error_rate:percentage > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate for {{ $labels.job }}"
          description: "Error rate is {{ $value }}% (threshold: 5%)"

      - alert: HighLatency
        expr: job:http_request_duration:p95 > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency for {{ $labels.job }}"
          description: "P95 latency is {{ $value }}s (threshold: 1s)"

  - name: resources
    interval: 1m
    rules:
      - alert: HighCPUUsage
        expr: instance:node_cpu:utilization > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is {{ $value }}%"

      - alert: HighMemoryUsage
        expr: instance:node_memory:utilization > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value }}%"

      - alert: DiskSpaceLow
        expr: instance:node_disk:utilization > 90
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Disk usage is {{ $value }}%"
```

## 검증

```bash
# Validate configuration
promtool check config prometheus.yml

# Validate rules
promtool check rules /etc/prometheus/rules/*.yml

# Test query
promtool query instant http://localhost:9090 'up'
```

**참조:** See `scripts/validate-prometheus.sh`

## 최선의 관행

1. **Use 일관된 naming** 위한 메트릭 (prefix_name_unit)
2. **세트 적절한 scrape intervals** (15-60s 일반적인)
3. **Use 기록 규칙** 위한 expensive 쿼리
4. **Implement high 가용성** (여러 Prometheus 인스턴스)
5. **Configure retention** based 에 스토리지 용량
6. **Use relabeling** 위한 metric cleanup
7. **모니터 Prometheus itself**
8. **Implement 연합** 위한 large deployments
9. **Use Thanos/Cortex** 위한 long-term 스토리지
10. **Document 사용자 정의 메트릭**

## 문제 해결

**Check scrape targets:**
```bash
curl http://localhost:9090/api/v1/targets
```

**Check 구성:**
```bash
curl http://localhost:9090/api/v1/status/config
```

**Test 쿼리:**
```bash
curl 'http://localhost:9090/api/v1/query?query=up'
```

## 참조 파일

- `assets/prometheus.yml.template` - 완전한 구성 템플릿
- `references/scrape-configs.md` - Scrape 구성 패턴
- `references/recording-rules.md` - 기록 규칙 예제
- `scripts/validate-prometheus.sh` - 검증 스크립트

## 관련됨 Skills

- `grafana-dashboards` - 위한 시각화
- `slo-implementation` - 위한 SLO 모니터링
- `distributed-tracing` - 위한 요청 추적
