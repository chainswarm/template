#!/usr/bin/env bash
#
# Start infrastructure services (PostgreSQL, Redis, ClickHouse)
#

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly INFRA_DIR="$PROJECT_ROOT/infrastructure"

# Colors for output
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker not found. Please install Docker first."
        exit 1
    fi

    if ! command -v docker compose &> /dev/null; then
        log_error "Docker Compose not found. Please install Docker Compose first."
        exit 1
    fi
}

check_env_file() {
    if [ ! -f "$INFRA_DIR/.env" ]; then
        log_warn ".env file not found in $INFRA_DIR"
        log_info "Copying .env.example to .env"
        cp "$INFRA_DIR/.env.example" "$INFRA_DIR/.env"
        log_warn "Please review and update $INFRA_DIR/.env with your configuration"
    fi
}

start_infrastructure() {
    log_info "Starting infrastructure services..."
    
    cd "$INFRA_DIR"
    
    # Start services
    docker compose up -d
    
    log_info "Infrastructure services started"
    echo ""
    log_info "Services:"
    log_info " - PostgreSQL:        localhost:5432"
    log_info " - Redis:             localhost:6379"
    log_info " - ClickHouse HTTP:   localhost:8123"
    log_info " - ClickHouse Native: localhost:9000"
    echo ""
    log_info "Check service status: cd infrastructure && docker compose ps"
    log_info "View logs:            cd infrastructure && docker compose logs -f"
}

main() {
    log_info "Infrastructure startup script"
    echo ""
    
    check_prerequisites
    check_env_file
    start_infrastructure
    
    echo ""
    log_info "Infrastructure setup complete!"
}

main "$@"
