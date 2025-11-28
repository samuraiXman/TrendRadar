# coding=utf-8
import os
from typing import Dict, List, Optional, Tuple, Union
from .external_sources_simple import (
    YouTubeTrendingSource,
    CNNNewsSource,
    NewsAPISource,
    HackerNewsSource,
)


class ExternalSourceAdapter:
    """外部数据源适配器 - 与 DataFetcher 兼容"""

    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        self.external_sources = {}
        self._initialize_sources()

    def _initialize_sources(self):
        """初始化配置的外部数据源"""
        # YouTube - 总是添加，即使没有 API Key 也会返回空数据
        self.external_sources["youtube-trending"] = YouTubeTrendingSource(
            api_key=os.environ.get("YOUTUBE_API_KEY"),
            proxy_url=self.proxy_url
        )
        print("✅ YouTube 数据源已初始化")

        # CNN 新闻 - 无需 API Key
        self.external_sources["cnn-news"] = CNNNewsSource(
            proxy_url=self.proxy_url
        )
        print("✅ CNN 数据源已初始化")

        # NewsAPI 多源 - 总是添加，即使没有 API Key 也会返回空数据
        self.external_sources["newsapi-cnn-bbc"] = NewsAPISource(
            api_key=os.environ.get("NEWSAPI_KEY"),
            sources=["cnn", "bbc-news"],
            proxy_url=self.proxy_url
        )
        print("✅ NewsAPI (CNN + BBC) 数据源已初始化")

        # Hacker News - 无需 API Key
        self.external_sources["hackernews"] = HackerNewsSource(
            proxy_url=self.proxy_url
        )
        print("✅ Hacker News 数据源已初始化")

    def fetch_external_data(self, source_id: str) -> Tuple[Optional[str], str, str]:
        """
        获取外部数据源数据
        
        Args:
            source_id: 数据源 ID (如 'youtube-trending', 'cnn-news')
            
        Returns:
            (json_response, source_id, source_name) 元组，与 DataFetcher.fetch_data 格式一致
        """
        if source_id not in self.external_sources:
            return None, source_id, source_id

        try:
            source = self.external_sources[source_id]
            data = source.fetch_data()
            
            # 如果状态是 "skip"，则跳过（没有输出任何信息）
            if data.get("status") == "skip":
                return None, source_id, source_id
            
            # 转换为 JSON 字符串（与 newsnow 格式一致）
            import json
            json_str = json.dumps({
                "status": data.get("status"),
                "items": data.get("items", [])
            })
            
            # 生成友好的名称
            source_names = {
                "youtube-trending": "YouTube 热门",
                "cnn-news": "CNN 新闻",
                "newsapi-cnn-bbc": "新闻聚合 (CNN/BBC)",
                "hackernews": "Hacker News",
            }
            source_name = source_names.get(source_id, source_id)
            
            return json_str, source_id, source_name
            
        except Exception as e:
            print(f"❌ 获取 {source_id} 失败: {e}")
            return None, source_id, source_id

    def is_external_source(self, source_id: str) -> bool:
        """检查是否为外部数据源"""
        return source_id in self.external_sources or source_id in [
            "youtube-trending", "cnn-news", "newsapi-cnn-bbc", "hackernews"
        ]

    def get_available_sources(self) -> List[str]:
        """获取所有可用的外部数据源"""
        return [
            "youtube-trending",  # 需要 YOUTUBE_API_KEY
            "cnn-news",           # 无需 API Key
            "newsapi-cnn-bbc",    # 需要 NEWSAPI_KEY
            "hackernews",         # 无需 API Key
        ]


# 全局适配器实例
_adapter_instance: Optional[ExternalSourceAdapter] = None


def get_adapter(proxy_url: Optional[str] = None) -> ExternalSourceAdapter:
    """获取全局适配器实例（单例）"""
    global _adapter_instance
    if _adapter_instance is None:
        _adapter_instance = ExternalSourceAdapter(proxy_url)
    return _adapter_instance

