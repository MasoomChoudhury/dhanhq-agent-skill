#!/usr/bin/env python3
"""
DhanHQ Instrument Lookup Tool
==============================
Queries the DhanHQ instrument master CSV using DuckDB — zero full-file loading.
DuckDB reads only the rows/columns needed for your query, making it safe for
agent use even though the CSV has 100,000+ instruments.

IMPORTANT: Always run `refresh` first at the start of any session.
The instrument master changes daily (new expiries, new contracts).

Usage:
    python instrument_lookup.py <command> [args...]

Commands:
    refresh             ALWAYS RUN FIRST — downloads latest CSV from DhanHQ
    find_by_symbol      <symbol>                    Search by symbol name (partial match)
    find_equity         <symbol> [exchange]         Get equity security ID
    find_futures        <underlying> <expiry_flag>  Get futures contracts (W/M)
    find_options        <underlying> <expiry_date> <strike> <CE|PE>
    get_security_id     <trading_symbol>            Exact trading symbol lookup
    list_expiries       <underlying> [instrument]   All expiry dates for underlying
    segment_list        <segment>                   All instruments in a segment

Requirements:
    pip install duckdb
"""

import sys
import json
import os
import datetime
import duckdb

# ── Config ────────────────────────────────────────────────────────────────────
COMPACT_URL   = "https://images.dhan.co/api-data/api-scrip-master.csv"
DETAILED_URL  = "https://images.dhan.co/api-data/api-scrip-master-detailed.csv"
CACHE_DIR     = os.path.join(os.path.dirname(__file__), ".cache")
COMPACT_CACHE = os.path.join(CACHE_DIR, "scrip_master.csv")
DETAILED_CACHE= os.path.join(CACHE_DIR, "scrip_master_detailed.csv")
CACHE_TTL_HRS = 6   # Refresh cache every 6 hours

# ── Cache management ──────────────────────────────────────────────────────────
def _is_cache_fresh(path: str) -> bool:
    if not os.path.exists(path):
        return False
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    return (datetime.datetime.now() - mtime).total_seconds() < CACHE_TTL_HRS * 3600

def ensure_cache(use_detailed: bool = False) -> str:
    """Download CSV if cache is stale. Returns local file path."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    url   = DETAILED_URL  if use_detailed else COMPACT_URL
    cache = DETAILED_CACHE if use_detailed else COMPACT_CACHE
    if not _is_cache_fresh(cache):
        import urllib.request
        print(f"[cache] Refreshing from {url} ...", file=sys.stderr)
        urllib.request.urlretrieve(url, cache)
        print(f"[cache] Saved to {cache}", file=sys.stderr)
    return cache


def force_refresh() -> dict:
    """Force-download the latest instrument master CSV, ignoring cache age.
    Always call this at the start of a session before any lookup queries.
    """
    import urllib.request
    os.makedirs(CACHE_DIR, exist_ok=True)
    results = {}
    for url, cache, label in [
        (COMPACT_URL,  COMPACT_CACHE,  "compact"),
        (DETAILED_URL, DETAILED_CACHE, "detailed"),
    ]:
        print(f"[refresh] Downloading {label} from {url} ...", file=sys.stderr)
        urllib.request.urlretrieve(url, cache)
        size_kb = os.path.getsize(cache) // 1024
        results[label] = {"status": "ok", "path": cache, "size_kb": size_kb}
        print(f"[refresh] {label} saved ({size_kb} KB)", file=sys.stderr)
    return {"status": "refreshed", "files": results,
            "timestamp": datetime.datetime.now().isoformat()}

# ── Query helpers ─────────────────────────────────────────────────────────────
def _run(sql: str, params=None) -> list[dict]:
    con = duckdb.connect()
    result = con.execute(sql, params or []).fetchdf()
    return result.to_dict(orient="records")

def _compact(path: str) -> str:
    """Reference to local compact CSV for DuckDB."""
    return f"read_csv_auto('{path}', header=true)"

def _detailed(path: str) -> str:
    return f"read_csv_auto('{path}', header=true)"

# ── Commands ──────────────────────────────────────────────────────────────────

def find_by_symbol(symbol: str, limit: int = 20) -> list[dict]:
    """Fuzzy symbol search — returns key fields only."""
    path = ensure_cache()
    sql = f"""
        SELECT
            SEM_EXM_EXCH_ID     AS exchange,
            SEM_SEGMENT         AS segment,
            SEM_SMST_SECURITY_ID AS security_id,
            SEM_INSTRUMENT_NAME AS instrument,
            SEM_CUSTOM_SYMBOL   AS display_name,
            SM_SYMBOL_NAME      AS symbol_name,
            SEM_EXPIRY_DATE     AS expiry_date,
            SEM_STRIKE_PRICE    AS strike_price,
            SEM_OPTION_TYPE     AS option_type,
            SEM_LOT_UNITS       AS lot_size
        FROM {_compact(path)}
        WHERE upper(SM_SYMBOL_NAME) LIKE upper('%' || ? || '%')
           OR upper(SEM_CUSTOM_SYMBOL) LIKE upper('%' || ? || '%')
        LIMIT {limit}
    """
    return _run(sql, [symbol, symbol])


def find_equity(symbol: str, exchange: str = "NSE") -> list[dict]:
    """Get equity instrument security ID."""
    path = ensure_cache()
    sql = f"""
        SELECT
            SEM_EXM_EXCH_ID     AS exchange,
            SEM_SMST_SECURITY_ID AS security_id,
            SEM_CUSTOM_SYMBOL   AS display_name,
            SM_SYMBOL_NAME      AS symbol_name,
            SEM_SEGMENT         AS segment,
            SEM_LOT_UNITS       AS lot_size,
            SEM_TICK_SIZE       AS tick_size
        FROM {_compact(path)}
        WHERE SEM_INSTRUMENT_NAME = 'EQUITY'
          AND upper(SEM_EXM_EXCH_ID) = upper(?)
          AND (upper(SM_SYMBOL_NAME) = upper(?) OR upper(SEM_CUSTOM_SYMBOL) = upper(?))
        LIMIT 5
    """
    return _run(sql, [exchange, symbol, symbol])


def find_futures(underlying: str, expiry_flag: str = "M") -> list[dict]:
    """Get futures contracts for an underlying. expiry_flag: M=Monthly, W=Weekly."""
    path = ensure_cache()
    sql = f"""
        SELECT
            SEM_EXM_EXCH_ID     AS exchange,
            SEM_SMST_SECURITY_ID AS security_id,
            SEM_INSTRUMENT_NAME AS instrument,
            SEM_CUSTOM_SYMBOL   AS display_name,
            SEM_EXPIRY_DATE     AS expiry_date,
            SEM_EXPIRY_CODE     AS expiry_code,
            SEM_EXPIRY_FLAG     AS expiry_flag,
            SEM_LOT_UNITS       AS lot_size
        FROM {_compact(path)}
        WHERE SEM_INSTRUMENT_NAME IN ('FUTIDX','FUTSTK','FUTCOM','FUTCUR')
          AND upper(SM_SYMBOL_NAME) = upper(?)
          AND upper(SEM_EXPIRY_FLAG) = upper(?)
        ORDER BY SEM_EXPIRY_DATE ASC
        LIMIT 10
    """
    return _run(sql, [underlying, expiry_flag])


def find_options(underlying: str, expiry_date: str, strike: float, option_type: str) -> list[dict]:
    """Find a specific option contract. option_type: CE or PE."""
    path = ensure_cache()
    sql = f"""
        SELECT
            SEM_EXM_EXCH_ID     AS exchange,
            SEM_SMST_SECURITY_ID AS security_id,
            SEM_INSTRUMENT_NAME AS instrument,
            SEM_CUSTOM_SYMBOL   AS display_name,
            SEM_EXPIRY_DATE     AS expiry_date,
            SEM_STRIKE_PRICE    AS strike_price,
            SEM_OPTION_TYPE     AS option_type,
            SEM_LOT_UNITS       AS lot_size,
            SEM_TICK_SIZE       AS tick_size
        FROM {_compact(path)}
        WHERE SEM_INSTRUMENT_NAME IN ('OPTIDX','OPTSTK','OPTCUR','OPTFUT')
          AND upper(SM_SYMBOL_NAME) = upper(?)
          AND SEM_EXPIRY_DATE LIKE ? || '%'
          AND ABS(SEM_STRIKE_PRICE - ?) < 0.01
          AND upper(SEM_OPTION_TYPE) = upper(?)
        LIMIT 5
    """
    return _run(sql, [underlying, expiry_date, strike, option_type])


def get_security_id(trading_symbol: str) -> list[dict]:
    """Exact trading symbol lookup — fastest single-instrument query."""
    path = ensure_cache()
    sql = f"""
        SELECT
            SEM_EXM_EXCH_ID     AS exchange,
            SEM_SMST_SECURITY_ID AS security_id,
            SEM_INSTRUMENT_NAME AS instrument,
            SEM_CUSTOM_SYMBOL   AS display_name,
            SEM_EXPIRY_DATE     AS expiry_date,
            SEM_STRIKE_PRICE    AS strike_price,
            SEM_OPTION_TYPE     AS option_type,
            SEM_LOT_UNITS       AS lot_size
        FROM {_compact(path)}
        WHERE upper(SEM_TRADING_SYMBOL) = upper(?)
        LIMIT 3
    """
    return _run(sql, [trading_symbol])


def list_expiries(underlying: str, instrument: str = "OPTIDX") -> list[dict]:
    """All unique expiry dates for an underlying instrument."""
    path = ensure_cache()
    sql = f"""
        SELECT DISTINCT
            SEM_EXPIRY_DATE  AS expiry_date,
            SEM_EXPIRY_FLAG  AS expiry_flag,
            SEM_EXPIRY_CODE  AS expiry_code
        FROM {_compact(path)}
        WHERE upper(SM_SYMBOL_NAME) = upper(?)
          AND upper(SEM_INSTRUMENT_NAME) = upper(?)
        ORDER BY SEM_EXPIRY_DATE ASC
    """
    return _run(sql, [underlying, instrument])


def segment_list(exchange_segment: str, limit: int = 50) -> list[dict]:
    """All active instruments in a given exchange segment."""
    # Map composite segment strings to column filters
    seg_map = {
        "NSE_EQ":       ("NSE", "E"),
        "NSE_FNO":      ("NSE", "D"),
        "NSE_CURRENCY": ("NSE", "C"),
        "BSE_EQ":       ("BSE", "E"),
        "BSE_FNO":      ("BSE", "D"),
        "BSE_CURRENCY": ("BSE", "C"),
        "MCX_COMM":     ("MCX", "M"),
    }
    if exchange_segment.upper() not in seg_map:
        return [{"error": f"Unknown segment. Valid: {list(seg_map.keys())}"}]
    exch, seg = seg_map[exchange_segment.upper()]
    path = ensure_cache()
    sql = f"""
        SELECT
            SEM_SMST_SECURITY_ID AS security_id,
            SEM_INSTRUMENT_NAME AS instrument,
            SEM_CUSTOM_SYMBOL   AS display_name,
            SM_SYMBOL_NAME      AS symbol_name,
            SEM_LOT_UNITS       AS lot_size,
            SEM_EXPIRY_DATE     AS expiry_date,
            SEM_STRIKE_PRICE    AS strike_price,
            SEM_OPTION_TYPE     AS option_type
        FROM {_compact(path)}
        WHERE upper(SEM_EXM_EXCH_ID) = upper(?)
          AND SEM_SEGMENT = ?
        LIMIT {limit}
    """
    return _run(sql, [exch, seg])


# ── CLI dispatcher ─────────────────────────────────────────────────────────────
COMMANDS = {
    "refresh":        lambda args: force_refresh(),
    "find_by_symbol": lambda args: find_by_symbol(args[0]),
    "find_equity":    lambda args: find_equity(args[0], args[1] if len(args) > 1 else "NSE"),
    "find_futures":   lambda args: find_futures(args[0], args[1] if len(args) > 1 else "M"),
    "find_options":   lambda args: find_options(args[0], args[1], float(args[2]), args[3]),
    "get_security_id":lambda args: get_security_id(args[0]),
    "list_expiries":  lambda args: list_expiries(args[0], args[1] if len(args) > 1 else "OPTIDX"),
    "segment_list":   lambda args: segment_list(args[0]),
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(f"Usage: python instrument_lookup.py <command> [args...]\nCommands: {list(COMMANDS.keys())}")
        sys.exit(1)
    cmd  = sys.argv[1]
    args = sys.argv[2:]
    try:
        result = COMMANDS[cmd](args)
        print(json.dumps(result, indent=2, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
