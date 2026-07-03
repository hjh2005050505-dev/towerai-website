from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

@lru_cache(maxsize=1)
def load_products() -> list[dict[str, Any]]:
    return json.loads((DATA_DIR / "products.json").read_text(encoding="utf-8"))

@lru_cache(maxsize=1)
def load_scenarios() -> list[dict[str, Any]]:
    return json.loads((DATA_DIR / "scenarios.json").read_text(encoding="utf-8"))

def all_knowledge_items() -> list[dict[str, Any]]:
    products = [{"type": "product", "title": item["name"], "summary": item["summary"], "keywords": item.get("keywords", []), "features": item.get("features", []), "value": item.get("value", "")} for item in load_products()]
    scenarios = [{"type": "scenario", "title": item["name"], "summary": item["summary"], "keywords": item.get("keywords", []), "features": item.get("capabilities", []), "value": item.get("value", ""), "flow": item.get("flow", [])} for item in load_scenarios()]
    return products + scenarios

def search_knowledge(query: str, limit: int = 3) -> list[dict[str, Any]]:
    query_lower = query.lower()
    scored: list[tuple[int, dict[str, Any]]] = []
    for item in all_knowledge_items():
        haystack = " ".join([item["title"], item["summary"], " ".join(item.get("keywords", [])), " ".join(item.get("features", [])), item.get("value", ""), " ".join(item.get("flow", []))]).lower()
        score = 0
        for token in _tokens(query_lower):
            if token in haystack:
                score += 2 if token in item["title"].lower() else 1
        for keyword in item.get("keywords", []):
            if keyword.lower() in query_lower:
                score += 3
        if score:
            scored.append((score, item))
    scored.sort(key=lambda row: row[0], reverse=True)
    return [item for _, item in scored[:limit]]

def _tokens(text: str) -> list[str]:
    separators = "，。！？、；：,.!?;:()[]{} \n\t"
    for char in separators:
        text = text.replace(char, " ")
    return [token for token in text.split(" ") if len(token.strip()) >= 2]
