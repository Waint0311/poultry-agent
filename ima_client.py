# -*- coding: utf-8 -*-
"""
ima 知识库检索客户端
通过 ima Agent 接口（OpenAPI）检索《禽病》知识库

凭证来源：https://ima.qq.com/agent-interface 生成
  - X-Client-Id
  - X-Api-Key

⚠️ 说明：ima OpenAPI 的精确请求格式以官方文档为准。
如果接口调用失败或未配置凭证，search() 返回 None，
上层应用会自动降级为"无知识库检索"的纯模型回答。
"""

import os
import requests

IMA_CLIENT_ID = os.getenv("IMA_CLIENT_ID", "")
IMA_API_KEY = os.getenv("IMA_API_KEY", "")
IMA_API_BASE = os.getenv("IMA_API_BASE", "https://api.ima.qq.com")  # 以官方文档为准


class ImaClient:
    """ima 知识库检索客户端（轻量封装）"""

    def __init__(self, client_id: str = None, api_key: str = None, api_base: str = None):
        self.client_id = client_id or IMA_CLIENT_ID
        self.api_key = api_key or IMA_API_KEY
        self.api_base = api_base or IMA_API_BASE

    def available(self) -> bool:
        """是否配置了凭证"""
        return bool(self.client_id and self.api_key)

    def list_knowledge_bases(self):
        """获取知识库列表"""
        if not self.available():
            return None
        # TODO: 按 ima 官方 OpenAPI 文档实现
        # 示例请求（占位）：
        # url = f"{self.api_base}/v1/knowledge-bases"
        # headers = {"X-Client-Id": self.client_id, "X-Api-Key": self.api_key}
        # return requests.get(url, headers=headers, timeout=10).json()
        return None

    def search(self, query: str, top_k: int = 3):
        """检索知识库，返回命中的文本片段列表；失败返回 None"""
        if not self.available():
            return None
        try:
            # TODO: 按 ima 官方 OpenAPI 文档实现检索端点
            # url = f"{self.api_base}/v1/search"
            # payload = {"query": query, "top_k": top_k}
            # headers = {"X-Client-Id": self.client_id, "X-Api-Key": self.api_key, "Content-Type": "application/json"}
            # resp = requests.post(url, json=payload, headers=headers, timeout=15)
            # resp.raise_for_status()
            # data = resp.json()
            # return [item.get("text", "") for item in data.get("hits", [])]
            return None  # 未实现前返回 None，上层降级
        except Exception:
            return None


def search_ima(query: str, top_k: int = 3):
    """快捷函数：检索 ima 知识库，返回拼接好的文本或 None"""
    client = ImaClient()
    hits = client.search(query, top_k=top_k)
    if not hits:
        return None
    return "\n".join(hits)
