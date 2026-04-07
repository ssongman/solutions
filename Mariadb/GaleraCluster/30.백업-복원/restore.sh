#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
# MariaDB Galera Cluster - 복원
# 사용법: ./restore.sh <백업파일.sql.gz> [DB명]
# 예시  : ./restore.sh backups/loadtest_20260407_120000.sql.gz loadtest
# ─────────────────────────────────────────────────────────
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "사용법: $0 <백업파일.sql.gz> [DB명]"
  exit 1
fi

BACKUP_GZ="$1"

if [[ ! -f "$BACKUP_GZ" ]]; then
  echo "[ERROR] 파일 없음: $BACKUP_GZ"
  exit 1
fi

# ── .env 로드 ──────────────────────────────────────────
ENV_FILE="$(dirname "$0")/../.env"
if [[ -f "$ENV_FILE" ]]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

HOST="${MARIA_HOST:-127.0.0.1}"
PORT="${MARIA_PORT:-3306}"
USER="${MARIA_USER:-root}"
PASS="${MARIA_PASSWORD:-}"

# DB명: 인자 > .env > 파일명에서 추출
if [[ $# -ge 2 ]]; then
  DB="$2"
else
  DB="${MARIA_DB:-$(basename "$BACKUP_GZ" | cut -d'_' -f1)}"
fi

echo "========================================"
echo "  MariaDB Galera 복원 시작"
echo "  Host  : $HOST:$PORT"
echo "  DB    : $DB"
echo "  파일  : $BACKUP_GZ"
echo "========================================"
echo ""
read -p "  위 설정으로 복원합니다. 계속할까요? (y/N) " confirm
[[ "$confirm" == "y" || "$confirm" == "Y" ]] || { echo "취소됨"; exit 0; }

# ── 압축 해제 ──────────────────────────────────────────
echo ""
echo "[1/4] 압축 해제..."
SQL_FILE="${BACKUP_GZ%.gz}"
gunzip -k "$BACKUP_GZ"           # -k: 원본 .gz 유지

# ── DB 생성 (없으면) ───────────────────────────────────
echo "[2/4] DB 준비 (CREATE DATABASE IF NOT EXISTS)..."
docker exec mariadb-client \
  mariadb -u"$USER" -p"$PASS" -h"$HOST" -P"$PORT" \
  -e "CREATE DATABASE IF NOT EXISTS \`$DB\` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;" 2>/dev/null

# ── 복원 (Galera: 1개 노드에만 → 자동 동기화) ─────────
echo "[3/4] 데이터 복원 중..."
docker exec -i mariadb-client \
  mariadb -u"$USER" -p"$PASS" -h"$HOST" -P"$PORT" \
  "$DB" < "$SQL_FILE"

# ── 임시 SQL 파일 삭제 ─────────────────────────────────
rm -f "$SQL_FILE"

# ── 복원 검증 ──────────────────────────────────────────
echo "[4/4] 복원 검증..."
echo ""
docker exec mariadb-client \
  mariadb -u"$USER" -p"$PASS" -h"$HOST" -P"$PORT" \
  --table -e "
    SELECT table_name AS '테이블',
           table_rows  AS '행 수(추정)',
           ROUND(data_length/1024, 1) AS '데이터(KB)'
    FROM information_schema.tables
    WHERE table_schema = '$DB'
    ORDER BY table_name;
  " 2>/dev/null

echo ""
echo "========================================"
echo "  복원 완료"
echo "  DB    : $DB"
echo "  ※ Galera가 나머지 노드에 자동 동기화합니다."
echo "========================================"
