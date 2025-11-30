---
name: distributed-tracing
description: Implement 분산 추적 와 함께 Jaeger 및 Tempo 에 track 요청 전반에 걸쳐 microservices 및 identify 성능 bottlenecks. Use 때 디버깅 microservices, analyzing 요청 흐릅니다, 또는 implementing observability 위한 분산 시스템.
---

# 분산 추적

Implement 분산 추적 와 함께 Jaeger 및 Tempo 위한 요청 흐름 visibility 전반에 걸쳐 microservices.

## Purpose

Track 요청 전반에 걸쳐 분산 시스템 에 understand 지연 시간, 종속성, 및 실패 points.

## 때 에 Use

- Debug 지연 시간 이슈
- Understand 서비스 종속성
- Identify bottlenecks
- Trace 오류 전파
- Analyze 요청 경로

## 분산 추적 개념

### Trace 구조
```
Trace (Request ID: abc123)
  ↓
Span (frontend) [100ms]
  ↓
Span (api-gateway) [80ms]
  ├→ Span (auth-service) [10ms]
  └→ Span (user-service) [60ms]
      └→ Span (database) [40ms]
```

### 키 컴포넌트
- **Trace** - End-에-end 요청 journey
- **Span** - Single 연산 내에 a trace
- **컨텍스트** - 메타데이터 전파된 사이 서비스
- **태그합니다** - 키-값 쌍 위한 필터링
- **로깅합니다** - Timestamped 이벤트 내에 a span

## Jaeger 설정

### Kubernetes 배포

```bash
# Deploy Jaeger Operator
kubectl create namespace observability
kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.51.0/jaeger-operator.yaml -n observability

# Deploy Jaeger instance
kubectl apply -f - <<EOF
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: jaeger
  namespace: observability
spec:
  strategy: production
  storage:
    type: elasticsearch
    options:
      es:
        server-urls: http://elasticsearch:9200
  ingress:
    enabled: true
EOF
```

### Docker Compose

```yaml
version: '3.8'
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "5775:5775/udp"
      - "6831:6831/udp"
      - "6832:6832/udp"
      - "5778:5778"
      - "16686:16686"  # UI
      - "14268:14268"  # Collector
      - "14250:14250"  # gRPC
      - "9411:9411"    # Zipkin
    environment:
      - COLLECTOR_ZIPKIN_HOST_PORT=:9411
```

**참조:** See `references/jaeger-setup.md`

## 애플리케이션 Instrumentation

### OpenTelemetry (권장됨)

#### Python (Flask)
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask

# Initialize tracer
resource = Resource(attributes={SERVICE_NAME: "my-service"})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Instrument Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route('/api/users')
def get_users():
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("get_users") as span:
        span.set_attribute("user.count", 100)
        # Business logic
        users = fetch_users_from_db()
        return {"users": users}

def fetch_users_from_db():
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("database_query") as span:
        span.set_attribute("db.system", "postgresql")
        span.set_attribute("db.statement", "SELECT * FROM users")
        # Database query
        return query_database()
```

#### Node.js (Express)
```javascript
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');
const { BatchSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { registerInstrumentations } = require('@opentelemetry/instrumentation');
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');
const { ExpressInstrumentation } = require('@opentelemetry/instrumentation-express');

// Initialize tracer
const provider = new NodeTracerProvider({
  resource: { attributes: { 'service.name': 'my-service' } }
});

const exporter = new JaegerExporter({
  endpoint: 'http://jaeger:14268/api/traces'
});

provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register();

// Instrument libraries
registerInstrumentations({
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
  ],
});

const express = require('express');
const app = express();

app.get('/api/users', async (req, res) => {
  const tracer = trace.getTracer('my-service');
  const span = tracer.startSpan('get_users');

  try {
    const users = await fetchUsers();
    span.setAttributes({ 'user.count': users.length });
    res.json({ users });
  } finally {
    span.end();
  }
});
```

#### Go
```go
package main

import (
    "context"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/jaeger"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.4.0"
)

func initTracer() (*sdktrace.TracerProvider, error) {
    exporter, err := jaeger.New(jaeger.WithCollectorEndpoint(
        jaeger.WithEndpoint("http://jaeger:14268/api/traces"),
    ))
    if err != nil {
        return nil, err
    }

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String("my-service"),
        )),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}

func getUsers(ctx context.Context) ([]User, error) {
    tracer := otel.Tracer("my-service")
    ctx, span := tracer.Start(ctx, "get_users")
    defer span.End()

    span.SetAttributes(attribute.String("user.filter", "active"))

    users, err := fetchUsersFromDB(ctx)
    if err != nil {
        span.RecordError(err)
        return nil, err
    }

    span.SetAttributes(attribute.Int("user.count", len(users)))
    return users, nil
}
```

**참조:** See `references/instrumentation.md`

## 컨텍스트 전파

### HTTP 헤더
```
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
tracestate: congo=t61rcWkgMzE
```

### 전파 에서 HTTP 요청

#### Python
```python
from opentelemetry.propagate import inject

headers = {}
inject(headers)  # Injects trace context

response = requests.get('http://downstream-service/api', headers=headers)
```

#### Node.js
```javascript
const { propagation } = require('@opentelemetry/api');

const headers = {};
propagation.inject(context.active(), headers);

axios.get('http://downstream-service/api', { headers });
```

## Tempo 설정 (Grafana)

### Kubernetes 배포

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tempo-config
data:
  tempo.yaml: |
    server:
      http_listen_port: 3200

    distributor:
      receivers:
        jaeger:
          protocols:
            thrift_http:
            grpc:
        otlp:
          protocols:
            http:
            grpc:

    storage:
      trace:
        backend: s3
        s3:
          bucket: tempo-traces
          endpoint: s3.amazonaws.com

    querier:
      frontend_worker:
        frontend_address: tempo-query-frontend:9095
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tempo
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: tempo
        image: grafana/tempo:latest
        args:
          - -config.file=/etc/tempo/tempo.yaml
        volumeMounts:
        - name: config
          mountPath: /etc/tempo
      volumes:
      - name: config
        configMap:
          name: tempo-config
```

**참조:** See `assets/jaeger-config.yaml.template`

## Sampling Strategies

### Probabilistic Sampling
```yaml
# Sample 1% of traces
sampler:
  type: probabilistic
  param: 0.01
```

### 속도 제한 Sampling
```yaml
# Sample max 100 traces per second
sampler:
  type: ratelimiting
  param: 100
```

### Adaptive Sampling
```python
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased

# Sample based on trace ID (deterministic)
sampler = ParentBased(root=TraceIdRatioBased(0.01))
```

## Trace 분석

### 찾는 Slow 요청

**Jaeger 쿼리:**
```
service=my-service
duration > 1s
```

### 찾는 오류

**Jaeger 쿼리:**
```
service=my-service
error=true
tags.http.status_code >= 500
```

### 서비스 종속성 그래프

Jaeger automatically 생성합니다 서비스 종속성 그래프 표시하는:
- 서비스 관계
- 요청 평가합니다
- 오류 평가합니다
- 평균 latencies

## 최선의 관행

1. **샘플 적절하게** (1-10% 에서 production)
2. **Add 의미 있는 태그합니다** (user_id, request_id)
3. **Propagate 컨텍스트** 전반에 걸쳐 모든 서비스 boundaries
4. **Log 예외** 에서 spans
5. **Use 일관된 naming** 위한 작업
6. **모니터 추적 overhead** (<1% CPU impact)
7. **세트 up 경고** 위한 trace 오류
8. **Implement 분산 컨텍스트** (baggage)
9. **Use span 이벤트** 위한 중요한 milestones
10. **Document instrumentation** 표준

## 통합 와 함께 로깅

### Correlated 로깅합니다
```python
import logging
from opentelemetry import trace

logger = logging.getLogger(__name__)

def process_request():
    span = trace.get_current_span()
    trace_id = span.get_span_context().trace_id

    logger.info(
        "Processing request",
        extra={"trace_id": format(trace_id, '032x')}
    )
```

## 문제 해결

**아니요 추적합니다 appearing:**
- Check collector 엔드포인트
- Verify 네트워크 connectivity
- Check sampling 구성
- Review 애플리케이션 로깅합니다

**High 지연 시간 overhead:**
- Reduce sampling rate
- Use batch span processor
- Check exporter 구성

## 참조 파일

- `references/jaeger-setup.md` - Jaeger installation
- `references/instrumentation.md` - Instrumentation 패턴
- `assets/jaeger-config.yaml.template` - Jaeger 구성

## 관련됨 Skills

- `prometheus-configuration` - 위한 메트릭
- `grafana-dashboards` - 위한 시각화
- `slo-implementation` - 위한 지연 시간 SLOs
