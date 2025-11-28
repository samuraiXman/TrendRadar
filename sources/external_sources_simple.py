# coding=utf-8
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime

class ExternalDataSource:
    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    def fetch_data(self) -> Dict:
        raise NotImplementedError

    @property
    def proxies(self):
        if self.proxy_url:
            return {"http": self.proxy_url, "https": self.proxy_url}
        return None


class YouTubeTrendingSource(ExternalDataSource):
    def __init__(self, api_key: Optional[str] = None, proxy_url: Optional[str] = None):
        super().__init__(proxy_url)
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"

    def fetch_data(self) -> Dict:
        if not self.api_key:
            # 这不是错误，只是没有配置
            return {"status": "skip", "error": "API Key not configured", "items": []}
        
        try:
            url = f"{self.base_url}/videos"
            params = {
                "part": "snippet,statistics",
                "chart": "mostPopular",
                "regionCode": "US",
                "maxResults": 20,
                "key": self.api_key
            }
            
            response = requests.get(url, params=params, headers=self.headers, proxies=self.proxies, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            items = []
            for video in data.get("items", []):
                snippet = video.get("snippet", {})
                items.append({
                    "title": snippet.get("title", ""),
                    "url": f"https://www.youtube.com/watch?v={video.get('id')}",
                    "mobileUrl": f"https://youtu.be/{video.get('id')}",
                })
            
            print(f"YouTube: fetched {len(items)} videos")
            return {"status": "success", "items": items, "source": "youtube"}
        except Exception as e:
            print(f"YouTube fetch failed: {e}")
            return {"status": "error", "error": str(e), "items": []}


class CNNNewsSource(ExternalDataSource):
    def __init__(self, proxy_url: Optional[str] = None):
        super().__init__(proxy_url)

    def fetch_data(self) -> Dict:
        try:
            # 尝试多个 CNN RSS URL
            rss_urls = [
                "https://feeds.cnn.com/rss/cnn_topstories.rss",
                "http://rss.cnn.com/rss/edition.rss",
                "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            ]
            
            items = []
            for rss_url in rss_urls:
                try:
                    response = requests.get(rss_url, headers=self.headers, proxies=self.proxies, timeout=10)
                    response.raise_for_status()
                    
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(response.content)
                    
                    for item in root.findall(".//item")[:15]:
                        title_elem = item.find("title")
                        link_elem = item.find("link")
                        if title_elem is not None and title_elem.text:
                            items.append({
                                "title": title_elem.text.strip(),
                                "url": link_elem.text if link_elem is not None else "",
                                "mobileUrl": link_elem.text if link_elem is not None else "",
                            })
                    
                    if items:
                        print(f"CNN: fetched {len(items)} news from {rss_url}")
                        return {"status": "success", "items": items, "source": "cnn"}
                except:
                    continue
            
            # 如果所有 URL 都失败，返回空结果
            print(f"CNN: could not fetch news (all RSS URLs failed)")
            return {"status": "error", "error": "All RSS URLs failed", "items": []}
            
        except Exception as e:
            print(f"CNN fetch failed: {e}")
            return {"status": "error", "error": str(e), "items": []}


class HackerNewsSource(ExternalDataSource):
    def __init__(self, proxy_url: Optional[str] = None):
        super().__init__(proxy_url)
        self.base_url = "https://hacker-news.firebaseio.com/v0"

    def fetch_data(self) -> Dict:
        try:
            url = f"{self.base_url}/topstories.json"
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=15)
            response.raise_for_status()
            top_story_ids = response.json()[:50]
            
            items = []
            for story_id in top_story_ids[:15]:
                story_url = f"{self.base_url}/item/{story_id}.json"
                story_response = requests.get(story_url, headers=self.headers, proxies=self.proxies, timeout=10)
                story_response.raise_for_status()
                story = story_response.json()
                
                if story.get("type") == "story" and story.get("title"):
                    items.append({
                        "title": story.get("title", ""),
                        "url": story.get("url", ""),
                        "mobileUrl": story.get("url", ""),
                    })
            
            print(f"Hacker News: fetched {len(items)} stories")
            return {"status": "success", "items": items, "source": "hackernews"}
        except Exception as e:
            print(f"Hacker News fetch failed: {e}")
            return {"status": "error", "error": str(e), "items": []}


class NewsAPISource(ExternalDataSource):
    def __init__(self, api_key: Optional[str] = None, sources: Optional[List[str]] = None, proxy_url: Optional[str] = None):
        super().__init__(proxy_url)
        self.api_key = api_key
        self.sources = sources or ["cnn", "bbc-news"]
        self.base_url = "https://newsapi.org/v2"

    def fetch_data(self) -> Dict:
        if not self.api_key:
            # 这不是错误，只是没有配置
            return {"status": "skip", "error": "API Key not configured", "items": []}
        
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                "sources": ",".join(self.sources),
                "sortBy": "publishedAt",
                "apiKey": self.api_key,
                "pageSize": 20
            }
            
            response = requests.get(url, params=params, headers=self.headers, proxies=self.proxies, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "ok":
                return {"status": "error", "error": data.get("message", "Unknown error"), "items": []}
            
            items = []
            for article in data.get("articles", []):
                items.append({
                    "title": article.get("title", ""),
                    "url": article.get("url", ""),
                    "mobileUrl": article.get("url", ""),
                })
            
            print(f"NewsAPI: fetched {len(items)} articles")
            return {"status": "success", "items": items, "source": "newsapi"}
        except Exception as e:
            print(f"NewsAPI fetch failed: {e}")
            return {"status": "error", "error": str(e), "items": []}

