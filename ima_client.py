# -*- coding: utf-8 -*-
"""
ima 知识库检索客户端
通过 ima 官方 OpenAPI 检索《禽病》知识库

凭证来源：https://ima.qq.com/agent-interface 生成
  - X-Client-Id
  - X-Api-Key

接口文档：POST https://ima.qq.com/openapi/wiki/v1/*
认证 Header：ima-openapi-clientid / ima-openapi-apikey
响应格式：{ "retcode": 0, "errmsg": "成功", "data": {...} }
"""

import os
import requests

IMA_CLIENT_ID = os.getenv("IMA_CLIENT_ID", "")
IMA_API_KEY = os.getenv("IMA_API_KEY", "")
IMA_API_BASE = os.getenv("IMA_API_BASE", "https://ima.qq.com/openapi/wiki/v1")
IMA_KB_NAME = os.getenv("IMA_KB_NAME", "禽病")  # 目标知识库名称关键词（默认《禽病》）


class ImaClient:
    """ima 知识库检索客户端"""

    def __init__(self, client_id: str = None, api_key: str = None, kb_name: str = None):
        self.client_id = client_id or IMA_CLIENT_ID
        self.api_key = api_key or IMA_API_KEY
        self.kb_name = kb_name or IMA_KB_NAME
        self._kb_id = None  # 缓存知识库 ID

    def available(self) -> bool:
        return bool(self.client_id and self.api_key)

    def _headers(self) -> dict:
        return {
            "ima-openapi-clientid": self.client_id,
            "ima-openapi-apikey": self.api_key,
            "Content-Type": "application/json",
        }

    def _post(self, endpoint: str, payload: dict) -> dict:
        """POST 请求并解析统一响应结构（code=0 成功）"""
        resp = requests.post(
            f"{IMA_API_BASE}/{endpoint}",
            json=payload,
            headers=self._headers(),
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"ima API 错误: {data.get('msg')}")
        return data.get("data", {})

    def find_knowledge_base(self, name: str = None) -> str:
        """按名称搜索知识库，返回第一个匹配的知识库 ID"""
        query = name or self.kb_name
        data = self._post("search_knowledge_base", {"query": query, "cursor": "", "limit": 10})
        for kb in data.get("info_list", []):
            if query.lower() in kb.get("kb_name", "").lower():
                return kb.get("kb_id")
        lst = data.get("info_list", [])
        return lst[0]["kb_id"] if lst else None

    def search(self, query: str, top_k: int = 3):
        """在《禽病》知识库中检索，返回命中片段列表；失败返回 None"""
        if not self.available():
            return None
        try:
            if not self._kb_id:
                self._kb_id = self.find_knowledge_base()
            if not self._kb_id:
                return None

            data = self._post("search_knowledge", {
                "query": query,
                "cursor": "",
                "knowledge_base_id": self._kb_id,
            })

            results = []
            for hit in data.get("info_list", [])[:top_k]:
                title = hit.get("title", "").strip()
                content = hit.get("highlight_content", "").strip()
                if not title:
                    continue
                results.append(f"《{title}》" + (f"：{content}" if content else ""))
            return results if results else None
        except Exception:
            return None


def search_ima(query: str, top_k: int = 3):
    """快捷函数：检索 ima 知识库，返回拼接好的文本或 None"""
    client = ImaClient()
    hits = client.search(query, top_k=top_k)
    if not hits:
        return None
    return "\n\n".join(hits)


# 常见禽病关键词（用于多词轮询检索，提高命中率）
DISEASE_KEYWORDS = [
    "球虫", "新城疫", "禽流感", "鸡白痢", "沙门氏菌", "大肠杆菌",
    "传支", "传染性支气管炎", "法氏囊", "马立克", "支原体", "呼吸道",
    "鸭瘟", "鹅瘟", "小鹅瘟", "鸭病毒性肝炎", "产蛋下降", "寄生虫",
]


def search_ima_multi(query: str, top_k: int = 3):
    """多词检索：先用完整 query，再尝试疾病关键词，合并去重"""
    client = ImaClient()
    results = []
    seen = set()

    def _collect(hits):
        if not hits:
            return
        for h in hits:
            if h not in seen:
                seen.add(h)
                results.append(h)

    _collect(client.search(query, top_k=top_k))

    # 从 query 中匹配已知疾病关键词，逐个补充检索
    for kw in DISEASE_KEYWORDS:
        if len(results) >= top_k + 2:
            break
        if kw in query:
            _collect(client.search(kw, top_k=2))

    # 兜底：ima 按文档标题索引，宽泛词保证至少拿到真实文档池
    if len(results) < 2:
        _collect(client.search("禽病", top_k=3))
        _collect(client.search("鸡病", top_k=3))

    return "\n\n".join(results[:top_k + 2]) if results else None
