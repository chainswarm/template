#!/usr/bin/env bash
#
# Stop infrastructure services
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

stop_infrastructure() {
    log_info "Stopping infrastructure services..."
    
    cd "$INFRA_DIR"
    
    # Stop services
    docker compose down
    
    log_info "Infrastructure services stopped"
}

main() {
    log_info "Infrastructure shutdown script"
    echo ""
    
    stop_infrastructure
    
    echo ""
    log_info "Infrastructure shutdown complete!"
    log_warn "Note: Volumes are preserved. Data persists across restarts."
    log_info "To remove volumes: cd infrastructure && docker compose down -v"
}

main "$@"
