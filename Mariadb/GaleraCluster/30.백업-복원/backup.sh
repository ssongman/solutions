#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
# MariaDB Galera Cluster - 논리 백업 (mysqldump)
# 사용법: ./backup.sh [DB명]  (기본값: loadtest)
# ─────────────────────────────────────────────────────────
set -euo pipefail

# ── .env 로드 ──────────────────────────────────────────
ENV_FILE="$(dirname "$0")/../.env"
if [[ -f "$ENV_FILE" ]]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

HOST="${MARIA_HOST:-127.0.0.1}"
PORT="${MARIA_PORT:-3306}"
USER="${MARIA_USER:-root}"
PASS="${MARIA_PASSWORD:-}"
DB="${1:-${MARIA_DB:-loadtest}}"

# ── 백업 디렉토리 ──────────────────────────────────────
BACKUP_DIR="$(dirname "$0")/backups"
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/${DB}_${TIMESTAMP}.sql"
BACKUP_GZ="${BACKUP_FILE}.gz"

echo "========================================"
echo "  MariaDB Galera 백업 시작"
echo "  Host  : $HOST:$PORT"
echo "  DB    : $DB"
echo "  파일  : $BACKUP_GZ"
echo "========================================"

# ── wsrep_desync ON (백업 중 cluster flow control 방지) ─
echo "[1/4] wsrep_desync ON..."
docker exec mariadb-client \
  mariadb -u"$USER" -p"$PASS" -h"$HOST" -P"$PORT" \
  -e "SET GLOBAL wsrep_desync=ON;" 2>/dev/null

# ── mysqldump ──────────────────────────────────────────
echo "[2/4] mysqldump 실행..."
docker exec mariadb-client \
  mariadb-dump \
    -u"$USER" -p"$PASS" -h"$HOST" -P"$PORT" \
    --single-transaction \
    --routines \
    --triggers \
    --add-drop-table \
    --skip-lock-tables \
    "$DB" > "$BACKUP_FILE"

# ── 압축 ───────────────────────────────────────────────
echo "[3/4] gzip 압축..."
gzip "$BACKUP_FILE"

# ── wsrep_desync OFF ───────────────────────────────────
echo "[4/4] wsrep_desync OFF..."
docker exec mariadb-client \
  mariadb -u"$USER" -p"$PASS" -h"$HOST" -P"$PORT" \
  -e "SET GLOBAL wsrep_desync=OFF;" 2>/dev/null

# ── 결과 ───────────────────────────────────────────────
SIZE=$(du -sh "$BACKUP_GZ" | cut -f1)
echo ""
echo "========================================"
echo "  백업 완료"
echo "  파일 : $BACKUP_GZ"
echo "  크기 : $SIZE"
echo "========================================"
