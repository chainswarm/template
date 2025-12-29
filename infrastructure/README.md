# Infrastructure

Production-ready infrastructure services for agentic AI development.

## Services

### Core Services

| Service | Port | Purpose |
|---------|------|---------|
| **PostgreSQL** | 5432 | Relational database |
| **Redis** | 6379 | Cache and message broker |
| **ClickHouse** | 8123 (HTTP), 9000 (Native) | Analytics database |

### Observability Stack

| Service | Port | Purpose |
|---------|------|----------|
| **Prometheus** | 9090 | Metrics collection |
| **Loki** | 3100 | Log aggregation |
| **Grafana** | 3001 | Visualization |
| **Promtail** | - | Log shipper |

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose V2

### Setup

**1. Create environment file:**
```bash
cp .env.example .env
```

**2. Start core services:**
```bash
docker compose up -d
```

**3. Start observability (optional):**
```bash
cd observability
docker compose up -d
```

**OR use helper scripts:**
```bash
# From project root
bash scripts/dev/start-infra.sh
```

### Verify Services

```bash
# Check service status
docker compose ps

# View logs
docker compose logs -f postgres
docker compose logs -f redis
docker compose logs -f clickhouse
```

## Service Details

### PostgreSQL

**Connection String:**
```
postgresql://dev:dev_password@localhost:5432/myapp
```

**Connect with psql:**
```bash
docker exec -it infra-postgres psql -U dev -d myapp
```

**Python connection:**
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="myapp",
    user="dev",
    password="dev_password"
)
```

**Data Location:**
- Volume: `infra_postgres_data`
- Container path: `/var/lib/postgresql/data`

### Redis

**Connection String:**
```
redis://localhost:6379
```

**Connect with redis-cli:**
```bash
docker exec -it infra-redis redis-cli
```

**Python connection:**
```python
import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
```

**Data Location:**
- Volume: `infra_redis_data`
- Container path: `/data`

### ClickHouse

**HTTP Interface:**
```
http://localhost:8123
```

**Native Client:**
```
localhost:9000
```

**Connect with clickhouse-client:**
```bash
docker exec -it infra-clickhouse clickhouse-client
```

**Python connection:**
```python
from clickhouse_driver import Client

client = Client(
    host="localhost",
    port=9000,
    database="myapp"
)
```

**Web UI:**
- Play UI: http://localhost:8123/play
- Simple query interface built into ClickHouse

**Data Location:**
- Volume: `infra_clickhouse_data`
- Container path: `/var/lib/clickhouse`

## Observability Stack

### Prometheus

**Access:**
- URL: http://localhost:9090
- No authentication

**Metrics Endpoints:**

Add your application metrics endpoints to [`observability/prometheus/prometheus.yml`](observability/prometheus/prometheus.yml):

```yaml
scrape_configs:
  - job_name: 'my-app'
    static_configs:
      - targets: ['host.docker.internal:8000']
    metrics_path: '/metrics'
```

**Common Queries:**
```promql
# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### Loki

**Access:**
- URL: http://localhost:3100
- Query API: http://localhost:3100/loki/api/v1/query

**LogQL Queries:**
```logql
# All logs for a service
{service="my-service"}

# Error logs
{service="my-service"} |= "ERROR"

# JSON field filtering
{service="my-service"} | json | level="error"
```

### Grafana

**Access:**
- URL: http://localhost:3001
- Username: `admin`
- Password: `admin` (change on first login)

**Pre-configured Datasources:**
- Prometheus (default)
- Loki

**Creating Dashboards:**

1. Go to Dashboards → New Dashboard
2. Add Panel
3. Select Prometheus or Loki datasource
4. Write queries and configure visualization

**Import Dashboards:**

Import pre-built dashboards from [Grafana.com](https://grafana.com/grafana/dashboards/):

- Node Exporter: 1860
- Loki Dashboard: 13639
- ClickHouse: 14485

### Promtail

Promtail automatically ships logs to Loki.

**Log Locations:**
- Workspace logs: `../../logs/*.log`
- System logs: `/var/log/*.log`

**Configure in [`observability/promtail/promtail-config.yml`](observability/promtail/promtail-config.yml)**

## Network Architecture

### Core Services Network

```
infra_network (bridge)
├── postgres:5432
├── redis:6379
└── clickhouse:8123,9000
```

### Observability Network

```
observability_network (bridge)
├── prometheus:9090
├── loki:3100
├── grafana:3000 (exposed as 3001)
└── promtail
```

## Data Persistence

All data is persisted in named Docker volumes:

**Core Services:**
- `infra_postgres_data` - PostgreSQL data
- `infra_redis_data` - Redis data
- `infra_clickhouse_data` - ClickHouse data
- `infra_clickhouse_logs` - ClickHouse logs

**Observability:**
- `obs_prometheus_data` - Prometheus TSDB
- `obs_loki_data` - Loki chunks and indices
- `obs_grafana_data` - Grafana dashboards and settings

### Backup Data

```bash
# Backup PostgreSQL
docker exec infra-postgres pg_dump -U dev myapp > backup.sql

# Backup Redis
docker exec infra-redis redis-cli SAVE
docker cp infra-redis:/data/dump.rdb backup.rdb

# Backup ClickHouse
docker exec infra-clickhouse clickhouse-client --query "BACKUP TABLE mydb.mytable TO Disk('backups', 'backup.zip')"
```

### Restore Data

```bash
# Restore PostgreSQL
docker exec -i infra-postgres psql -U dev myapp < backup.sql

# Restore Redis
docker cp backup.rdb infra-redis:/data/dump.rdb
docker restart infra-redis
```

## Configuration

### Environment Variables

Edit `.env` file to configure services:

```bash
# PostgreSQL
POSTGRES_DB=myapp
POSTGRES_USER=dev
POSTGRES_PASSWORD=dev_password

# ClickHouse
CLICKHOUSE_DB=myapp
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=

# Observability
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
GRAFANA_ADMIN_PASSWORD=admin
```

### Service Configuration Files

- Prometheus: [`observability/prometheus/prometheus.yml`](observability/prometheus/prometheus.yml)
- Loki: [`observability/loki/loki-config.yml`](observability/loki/loki-config.yml)
- Promtail: [`observability/promtail/promtail-config.yml`](observability/promtail/promtail-config.yml)
- Grafana Datasources: [`observability/grafana/provisioning/datasources/datasources.yml`](observability/grafana/provisioning/datasources/datasources.yml)

## Troubleshooting

### Services Won't Start

**Check if ports are in use:**
```bash
# Linux/Mac
lsof -i :5432
lsof -i :6379
lsof -i :8123

# Windows
netstat -ano | findstr :5432
```

**View service logs:**
```bash
docker compose logs postgres
docker compose logs redis
docker compose logs clickhouse
```

**Restart services:**
```bash
docker compose restart postgres
# or restart all
docker compose restart
```

### Can't Connect to Services

**Check if services are running:**
```bash
docker compose ps
```

**Check Docker network:**
```bash
docker network inspect infra_network
```

**Test connectivity:**
```bash
# PostgreSQL
docker exec -it infra-postgres pg_isready

# Redis
docker exec -it infra-redis redis-cli ping

# ClickHouse
curl http://localhost:8123/ping
```

### Disk Space Issues

**Check volume sizes:**
```bash
docker system df -v
```

**Clean up old data:**
```bash
# Remove stopped containers
docker compose down

# Remove unused volumes (CAREFUL: This deletes data!)
docker volume prune
```

### Grafana Dashboards Not Showing Data

1. Check datasources: Configuration → Data Sources
2. Test connection to Prometheus/Loki
3. Verify metrics are being collected: http://localhost:9090/targets
4. Check time range in dashboard

## Maintenance

### Update Services

```bash
# Pull latest images
docker compose pull

# Restart with new images
docker compose up -d
```

### Clean Logs

```bash
# ClickHouse logs
docker exec infra-clickhouse find /var/log/clickhouse-server -name "*.log" -mtime +7 -delete

# Or configure log rotation in docker-compose.yml:
# logging:
#   driver: "json-file"
#   options:
#     max-size: "10m"
#     max-file: "3"
```

### Monitor Resource Usage

```bash
# Real-time stats
docker stats infra-postgres infra-redis infra-clickhouse

# Disk usage
docker system df
```

## Advanced

### Custom PostgreSQL Initialization

Create SQL files in `postgres/init/`:

```sql
-- postgres/init/01-create-tables.sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Mount in docker-compose.yml:
```yaml
postgres:
  volumes:
    - ./postgres/init:/docker-entrypoint-initdb.d
```

### ClickHouse Table Creation

```sql
CREATE TABLE IF NOT EXISTS events (
    timestamp DateTime,
    event_type String,
    user_id UInt64,
    data String
) ENGINE = MergeTree()
ORDER BY (timestamp, event_type);
```

### Redis Persistence Configuration

Edit docker-compose.yml:
```yaml
redis:
  command: redis-server --appendonly yes --save 60 1000
```

## See Also

- [`../roocode/automode.md`](../roocode/automode.md) - Execution patterns
- [`../libs/README.md`](../libs/README.md) - Core libraries
- [`../scripts/README.md`](../scripts/README.md) - Helper scripts
