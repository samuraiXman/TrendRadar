# coding=utf-8
from .external_sources_simple import (
    YouTubeTrendingSource,
    CNNNewsSource,
    NewsAPISource,
    HackerNewsSource,
)
from .adapter import ExternalSourceAdapter, get_adapter

__all__ = [
    "YouTubeTrendingSource",
    "CNNNewsSource",
    "NewsAPISource",
    "HackerNewsSource",
    "ExternalSourceAdapter",
    "get_adapter",
]

__version__ = "1.0.0"

