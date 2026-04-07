#!/usr/bin/env python3
"""
MariaDB Galera Cluster Load Test
- .env 파일에서 접속 정보 로드
- 동시 접속 부하 테스트 (INSERT / SELECT / UPDATE / DELETE)
- 노드별 분산 확인
- HTML 리포트 생성
"""

import pymysql
import threading
import time
import statistics
import os
import argparse
from datetime import datetime
from collections import defaultdict
from pathlib import Path

# ─────────────────────────────────────────
# .env 로드
# ─────────────────────────────────────────
def load_env(env_path=None):
    if env_path is None:
        env_path = Path(__file__).parent.parent / ".env"

    config = {}
    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    config[k.strip()] = v.strip()
    except FileNotFoundError:
        print(f"[WARN] .env 파일 없음: {env_path}")

    return {
        "host":     config.get("MARIA_HOST", "127.0.0.1"),
        "port":     int(config.get("MARIA_PORT", 3306)),
        "user":     config.get("MARIA_USER", "root"),
        "password": config.get("MARIA_PASSWORD", ""),
        "db":       config.get("MARIA_DB", "loadtest"),
    }


# ─────────────────────────────────────────
# DB 준비 (테스트용 DB / Table 생성)
# ─────────────────────────────────────────
def setup_db(config):
    conn = pymysql.connect(
        host=config["host"], port=config["port"],
        user=config["user"], password=config["password"],
        autocommit=True
    )
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {config['db']}")
        cur.execute(f"USE {config['db']}")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS load_test (
                id        BIGINT AUTO_INCREMENT PRIMARY KEY,
                thread_id INT,
                val       VARCHAR(64),
                score     INT,
                created   DATETIME DEFAULT NOW()
            )
        """)
        cur.execute("TRUNCATE TABLE load_test")
    conn.close()
    print(f"[SETUP] DB '{config['db']}' 및 테이블 준비 완료")


# ─────────────────────────────────────────
# 테스트 종료 후 정리
# ─────────────────────────────────────────
def teardown_db(config, drop=False):
    if not drop:
        return
    conn = pymysql.connect(
        host=config["host"], port=config["port"],
        user=config["user"], password=config["password"],
        autocommit=True
    )
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {config['db']}")
    conn.close()
    print(f"[TEARDOWN] DB '{config['db']}' 삭제 완료")


# ─────────────────────────────────────────
# Worker 스레드
# ─────────────────────────────────────────
def worker(config, stop_event, results, worker_id):
    latencies = defaultdict(list)  # op → [ms, ...]
    errors    = defaultdict(int)
    node_hits = defaultdict(int)   # hostname → count

    try:
        conn = pymysql.connect(
            host=config["host"], port=config["port"],
            user=config["user"], password=config["password"],
            database=config["db"],
            autocommit=True,
            connect_timeout=5
        )
    except Exception as e:
        results[worker_id] = {"error": str(e)}
        return

    # 접속 노드 확인
    with conn.cursor() as cur:
        cur.execute("SELECT @@hostname")
        node_hits[cur.fetchone()[0]] += 1

    last_id = None

    while not stop_event.is_set():
        # ── INSERT ──
        try:
            t0 = time.perf_counter()
            with conn.cursor() as cur:
                import random, string
                val = ''.join(random.choices(string.ascii_lowercase, k=16))
                score = random.randint(1, 1000)
                cur.execute(
                    "INSERT INTO load_test (thread_id, val, score) VALUES (%s, %s, %s)",
                    (worker_id, val, score)
                )
                last_id = cur.lastrowid
            latencies["INSERT"].append((time.perf_counter() - t0) * 1000)
        except Exception:
            errors["INSERT"] += 1

        # ── SELECT ──
        try:
            t0 = time.perf_counter()
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, val, score FROM load_test WHERE thread_id = %s ORDER BY id DESC LIMIT 10",
                    (worker_id,)
                )
                cur.fetchall()
                cur.execute("SELECT @@hostname")
                node_hits[cur.fetchone()[0]] += 1
            latencies["SELECT"].append((time.perf_counter() - t0) * 1000)
        except Exception:
            errors["SELECT"] += 1

        # ── UPDATE ──
        if last_id:
            try:
                t0 = time.perf_counter()
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE load_test SET score = score + 1 WHERE id = %s",
                        (last_id,)
                    )
                latencies["UPDATE"].append((time.perf_counter() - t0) * 1000)
            except Exception:
                errors["UPDATE"] += 1

        # ── DELETE (10% 확률) ──
        if last_id and random.random() < 0.1:
            try:
                t0 = time.perf_counter()
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM load_test WHERE id = %s", (last_id,))
                latencies["DELETE"].append((time.perf_counter() - t0) * 1000)
                last_id = None
            except Exception:
                errors["DELETE"] += 1

    conn.close()
    results[worker_id] = {"latencies": latencies, "errors": errors, "node_hits": node_hits}


# ─────────────────────────────────────────
# 통계 계산
# ─────────────────────────────────────────
def calc_stats(values):
    if not values:
        return {}
    sorted_v = sorted(values)
    return {
        "count": len(values),
        "avg":   round(statistics.mean(values), 2),
        "min":   round(min(values), 2),
        "max":   round(max(values), 2),
        "p50":   round(sorted_v[int(len(sorted_v) * 0.50)], 2),
        "p95":   round(sorted_v[int(len(sorted_v) * 0.95)], 2),
        "p99":   round(sorted_v[int(len(sorted_v) * 0.99)], 2),
    }


# ─────────────────────────────────────────
# HTML 리포트 생성
# ─────────────────────────────────────────
def generate_html_report(summary, config, args, duration):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_path = Path(__file__).parent / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    ops = ["INSERT", "SELECT", "UPDATE", "DELETE"]

    def stat_rows():
        rows = ""
        for op in ops:
            s = summary["stats"].get(op, {})
            if not s:
                continue
            rows += f"""
            <tr>
                <td><span class="badge badge-{op.lower()}">{op}</span></td>
                <td>{s.get('count', 0):,}</td>
                <td>{s.get('avg', '-')}</td>
                <td>{s.get('min', '-')}</td>
                <td>{s.get('max', '-')}</td>
                <td>{s.get('p50', '-')}</td>
                <td class="highlight">{s.get('p95', '-')}</td>
                <td class="highlight">{s.get('p99', '-')}</td>
            </tr>"""
        return rows

    def node_rows():
        rows = ""
        total = sum(summary["node_hits"].values()) or 1
        for node, cnt in sorted(summary["node_hits"].items()):
            pct = round(cnt / total * 100, 1)
            rows += f"""
            <tr>
                <td>{node}</td>
                <td>{cnt:,}</td>
                <td>
                    <div class="bar-wrap">
                        <div class="bar" style="width:{pct}%"></div>
                        <span>{pct}%</span>
                    </div>
                </td>
            </tr>"""
        return rows

    def error_rows():
        rows = ""
        for op, cnt in summary["errors"].items():
            if cnt:
                rows += f"<tr><td>{op}</td><td class='err'>{cnt}</td></tr>"
        return rows or "<tr><td colspan='2'>에러 없음</td></tr>"

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>MariaDB Galera 부하테스트 리포트</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', sans-serif; background: #f4f6f9; color: #333; padding: 30px; }}
  h1 {{ font-size: 1.6rem; margin-bottom: 4px; }}
  .subtitle {{ color: #666; font-size: 0.9rem; margin-bottom: 30px; }}
  .cards {{ display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 30px; }}
  .card {{ background: white; border-radius: 10px; padding: 20px 28px; flex: 1;
           min-width: 140px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
  .card .label {{ font-size: 0.78rem; color: #888; text-transform: uppercase; letter-spacing: .5px; }}
  .card .value {{ font-size: 2rem; font-weight: 700; color: #2563eb; margin-top: 4px; }}
  .card .unit  {{ font-size: 0.85rem; color: #555; }}
  section {{ background: white; border-radius: 10px; padding: 24px;
             box-shadow: 0 2px 8px rgba(0,0,0,.08); margin-bottom: 24px; }}
  h2 {{ font-size: 1.1rem; margin-bottom: 16px; border-left: 4px solid #2563eb;
        padding-left: 10px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
  th {{ background: #f8fafc; text-align: left; padding: 10px 14px;
        border-bottom: 2px solid #e2e8f0; color: #555; font-weight: 600; }}
  td {{ padding: 10px 14px; border-bottom: 1px solid #f0f0f0; }}
  tr:last-child td {{ border-bottom: none; }}
  .highlight {{ color: #dc2626; font-weight: 600; }}
  .err {{ color: #dc2626; font-weight: 700; }}
  .badge {{ display: inline-block; padding: 2px 10px; border-radius: 12px;
            font-size: 0.78rem; font-weight: 700; color: white; }}
  .badge-insert {{ background: #2563eb; }}
  .badge-select {{ background: #16a34a; }}
  .badge-update {{ background: #d97706; }}
  .badge-delete {{ background: #dc2626; }}
  .bar-wrap {{ display: flex; align-items: center; gap: 8px; }}
  .bar {{ height: 14px; background: #2563eb; border-radius: 4px; min-width: 4px; }}
  .config-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px,1fr)); gap: 10px; }}
  .cfg-item {{ background: #f8fafc; border-radius: 6px; padding: 10px 14px; font-size: 0.88rem; }}
  .cfg-item .k {{ color: #888; font-size: 0.78rem; }}
  .cfg-item .v {{ font-weight: 600; margin-top: 2px; }}
  footer {{ text-align: center; color: #aaa; font-size: 0.8rem; margin-top: 30px; }}
</style>
</head>
<body>

<h1>MariaDB Galera Cluster 부하테스트 리포트</h1>
<p class="subtitle">생성 시각: {ts}</p>

<div class="cards">
  <div class="card">
    <div class="label">총 쿼리</div>
    <div class="value">{summary['total_queries']:,}</div>
    <div class="unit">queries</div>
  </div>
  <div class="card">
    <div class="label">QPS</div>
    <div class="value">{summary['qps']}</div>
    <div class="unit">queries/sec</div>
  </div>
  <div class="card">
    <div class="label">TPS (트랜잭션)</div>
    <div class="value">{summary['tps']}</div>
    <div class="unit">tx/sec</div>
  </div>
  <div class="card">
    <div class="label">동시 접속</div>
    <div class="value">{args.workers}</div>
    <div class="unit">threads</div>
  </div>
  <div class="card">
    <div class="label">테스트 시간</div>
    <div class="value">{duration}</div>
    <div class="unit">초</div>
  </div>
  <div class="card">
    <div class="label">총 에러</div>
    <div class="value" style="color:{'#dc2626' if summary['total_errors'] else '#16a34a'}">{summary['total_errors']}</div>
    <div class="unit">errors</div>
  </div>
</div>

<section>
  <h2>오퍼레이션별 레이턴시 (ms)</h2>
  <table>
    <tr>
      <th>Operation</th><th>Count</th><th>Avg</th><th>Min</th><th>Max</th>
      <th>P50</th><th>P95</th><th>P99</th>
    </tr>
    {stat_rows()}
  </table>
</section>

<section>
  <h2>노드별 쿼리 분산</h2>
  <table>
    <tr><th>Node (hostname)</th><th>Hit Count</th><th>분산 비율</th></tr>
    {node_rows()}
  </table>
</section>

<section>
  <h2>에러 현황</h2>
  <table>
    <tr><th>Operation</th><th>Error Count</th></tr>
    {error_rows()}
  </table>
</section>

<section>
  <h2>테스트 설정</h2>
  <div class="config-grid">
    <div class="cfg-item"><div class="k">Host</div><div class="v">{config['host']}</div></div>
    <div class="cfg-item"><div class="k">Port</div><div class="v">{config['port']}</div></div>
    <div class="cfg-item"><div class="k">User</div><div class="v">{config['user']}</div></div>
    <div class="cfg-item"><div class="k">Database</div><div class="v">{config['db']}</div></div>
    <div class="cfg-item"><div class="k">Workers (Threads)</div><div class="v">{args.workers}</div></div>
    <div class="cfg-item"><div class="k">Duration</div><div class="v">{duration}s</div></div>
  </div>
</section>

<footer>MariaDB Galera Cluster Load Test · {ts}</footer>
</body>
</html>"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    return report_path


# ─────────────────────────────────────────
# Main
# ─────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="MariaDB Galera Cluster Load Test")
    parser.add_argument("--workers",  type=int,   default=10,    help="동시 접속 스레드 수 (default: 10)")
    parser.add_argument("--duration", type=int,   default=30,    help="테스트 시간(초) (default: 30)")
    parser.add_argument("--env",      type=str,   default=None,  help=".env 파일 경로")
    parser.add_argument("--drop",     action="store_true",       help="테스트 후 DB 삭제")
    args = parser.parse_args()

    config = load_env(args.env)

    print("=" * 60)
    print(f"  MariaDB Galera Cluster 부하 테스트")
    print(f"  Host   : {config['host']}:{config['port']}")
    print(f"  Workers: {args.workers} threads")
    print(f"  Duration: {args.duration}s")
    print("=" * 60)

    # DB 준비
    setup_db(config)

    # 워커 실행
    results    = {}
    stop_event = threading.Event()
    threads    = []

    print(f"\n[RUN] {args.workers}개 스레드 시작...")
    start_time = time.time()

    for i in range(args.workers):
        t = threading.Thread(target=worker, args=(config, stop_event, results, i))
        t.start()
        threads.append(t)

    # 진행 표시
    for elapsed in range(args.duration):
        time.sleep(1)
        print(f"  [{elapsed+1:3d}/{args.duration}s]", end="\r", flush=True)

    stop_event.set()
    for t in threads:
        t.join()

    actual_duration = round(time.time() - start_time, 1)
    print(f"\n[DONE] 실제 소요 시간: {actual_duration}s")

    # 결과 집계
    all_latencies = defaultdict(list)
    all_errors    = defaultdict(int)
    all_node_hits = defaultdict(int)

    for wid, res in results.items():
        if "error" in res:
            print(f"  [Worker {wid}] 연결 실패: {res['error']}")
            continue
        for op, lats in res["latencies"].items():
            all_latencies[op].extend(lats)
        for op, cnt in res["errors"].items():
            all_errors[op] += cnt
        for node, cnt in res["node_hits"].items():
            all_node_hits[node] += cnt

    total_queries = sum(len(v) for v in all_latencies.values())
    total_errors  = sum(all_errors.values())

    summary = {
        "total_queries": total_queries,
        "total_errors":  total_errors,
        "qps":           round(total_queries / actual_duration, 1),
        "tps":           round(all_latencies.get("INSERT", [0]).__len__() / actual_duration, 1),
        "stats":         {op: calc_stats(lats) for op, lats in all_latencies.items()},
        "errors":        dict(all_errors),
        "node_hits":     dict(all_node_hits),
    }

    # 콘솔 출력
    print("\n" + "=" * 60)
    print(f"  총 쿼리   : {summary['total_queries']:,}")
    print(f"  QPS       : {summary['qps']}")
    print(f"  총 에러   : {summary['total_errors']}")
    print()
    for op, s in summary["stats"].items():
        print(f"  [{op:6s}] count={s['count']:6,}  avg={s['avg']:7.2f}ms  p95={s['p95']:7.2f}ms  p99={s['p99']:7.2f}ms")
    print()
    print("  노드 분산:")
    total_hits = sum(summary["node_hits"].values()) or 1
    for node, cnt in sorted(summary["node_hits"].items()):
        print(f"    {node}: {cnt:,} ({cnt/total_hits*100:.1f}%)")
    print("=" * 60)

    # HTML 리포트 생성
    report_path = generate_html_report(summary, config, args, actual_duration)
    print(f"\n[REPORT] {report_path}")

    # 정리
    teardown_db(config, drop=args.drop)


if __name__ == "__main__":
    main()
