"""Vector Screener 直接进程内集成 — 零网络开销。

在 SimTradeLab 策略中直接调用 vector-screener 的选股函数，无需启动后端服务。

用法::

    from simtradelab.integrations.direct_screener import screen

    def handle_data(context, data):
        result = screen(date="2025-03-13", top_n=20)
        symbols = [s["symbol"] for s in result["stocks"]]
        set_universe(symbols)
"""

import sys
from pathlib import Path
from typing import Any, Optional

# 将 vector-screener 加入 Python 路径
_VS_ROOT = Path(__file__).resolve().parents[4] / "vector-screener"
if str(_VS_ROOT) not in sys.path:
    sys.path.insert(0, str(_VS_ROOT))

from backend.compute import screen as _screen_fn  # noqa: E402
from backend.data_sources import get_data_store  # noqa: E402

_store: Any = None  # DuckDBStore singleton


def _ensure_store():
    """确保 DuckDB 数据已加载（首次调用时加载，~18s）。"""
    global _store
    if _store is None:
        _store = get_data_store()
    return _store


def screen(
    *,
    date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    search: Optional[str] = None,
    period_conditions: Optional[str] = None,
    consecutive_conditions: Optional[str] = None,
    price_conditions: Optional[str] = None,
    min_volume: Optional[float] = None,
    sort_by: str = "change_pct",
    sort_order: str = "desc",
    top_n: int = 50,
    fields: Optional[list[str]] = None,
) -> dict:
    """直接调用 vector-screener 选股，返回与 API 一致的 dict。

    Args:
        date: 目标日期 "YYYY-MM-DD"，与 start_date/end_date 二选一
        start_date: 区间起始日期（与 date 二选一）
        end_date: 区间结束日期（与 date 二选一）
        search: 模糊搜索股票名称或代码
        period_conditions: 区间涨幅条件，如 "5d>10,20d<5"
        consecutive_conditions: 连续条件，如 "3d_2d>5"
        price_conditions: 价格条件，如 "close>10"
        min_volume: 最小成交量
        sort_by: 排序字段，默认 "change_pct"
        sort_order: "asc" 或 "desc"
        top_n: 返回前 N 只股票
        fields: 返回字段列表

    Returns:
        {"date": ..., "stocks": [...], "total": ..., ...}
    """
    _ensure_store()
    return _screen_fn(
        _store,
        date=date,
        start_date=start_date,
        end_date=end_date,
        search=search,
        period_conditions=period_conditions,
        consecutive_conditions=consecutive_conditions,
        price_conditions=price_conditions,
        min_volume=min_volume,
        sort_by=sort_by,
        sort_order=sort_order,
        page_size=top_n,
        fields=fields,
    )