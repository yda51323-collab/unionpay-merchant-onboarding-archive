# -*- coding: utf-8 -*-
"""unionpay-merchant-onboarding-archive 进件材料清单加载与校验。

校验：材料五类齐全、到期日是否临近、同商户号重复进件取最新。
"""
from __future__ import annotations

import csv
import datetime as dt
from collections import defaultdict
from typing import Dict, List

ARCHIVE_NAME = "unionpay-merchant-onboarding-archive"
CLIENT = "银联"
REQUIRED_DOCS = ("营业执照", "开户许可", "法人证件", "结算账户", "门店照")
EXPIRING_DAYS = 30


def load(path: str) -> List[dict]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _date(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def check_completeness(rows: List[dict]) -> Dict[str, dict]:
    """按商户号汇总已交材料，缺类标 incomplete。"""
    by_mch: Dict[str, dict] = defaultdict(lambda: {"docs": set(), "latest": None})
    for r in rows:
        slot = by_mch[r["mch_no"]]
        slot["docs"].add(r["doc_type"])
        submitted = r["submit_time"]
        if slot["latest"] is None or submitted > slot["latest"]:
            slot["latest"] = submitted
    out = {}
    for mch, slot in by_mch.items():
        missing = [d for d in REQUIRED_DOCS if d not in slot["docs"]]
        out[mch] = {
            "missing": missing,
            "status": "incomplete" if missing else "complete",
            "latest_submit": slot["latest"],
        }
    return out


def expiring(rows: List[dict], today: dt.date | None = None) -> List[dict]:
    today = today or dt.date.today()
    out = []
    for r in rows:
        left = (_date(r["expire_date"]) - today).days
        if 0 <= left <= EXPIRING_DAYS:
            out.append({"mch_no": r["mch_no"], "doc_type": r["doc_type"], "days_left": left})
    return sorted(out, key=lambda x: x["days_left"])
