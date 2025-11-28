# 🔧 集成外部数据源补丁

本文档说明如何修改 `main.py` 以集成外部数据源（YouTube、CNN 等）。

## 修改步骤

### 第 1 步：在 `DataFetcher` 类中添加外部适配器

**文件：** `main.py`  
**位置：** 约第 474 行（在 `__init__` 方法中）

**原代码：**
```python
class DataFetcher:
    """数据获取器"""

    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
```

**修改为：**
```python
class DataFetcher:
    """数据获取器"""

    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        
        # 添加外部数据源支持
        try:
            from sources.adapter import get_adapter
            self.external_adapter = get_adapter(proxy_url)
        except ImportError:
            self.external_adapter = None
            print("⚠️ 外部数据源模块未安装，跳过")
```

---

### 第 2 步：修改 `fetch_data` 方法

**文件：** `main.py`  
**位置：** 约第 477-535 行

**原代码：**
```python
def fetch_data(
    self,
    id_info: Union[str, Tuple[str, str]],
    max_retries: int = 2,
    min_retry_wait: int = 3,
    max_retry_wait: int = 5,
) -> Tuple[Optional[str], str, str]:
    """获取指定ID数据，支持重试"""
    if isinstance(id_info, tuple):
        id_value, alias = id_info
    else:
        id_value = id_info
        alias = id_value

    url = f"https://newsnow.busiyi.world/api/s?id={id_value}&latest"
    # ... 后续代码
```

**修改为：**
```python
def fetch_data(
    self,
    id_info: Union[str, Tuple[str, str]],
    max_retries: int = 2,
    min_retry_wait: int = 3,
    max_retry_wait: int = 5,
) -> Tuple[Optional[str], str, str]:
    """获取指定ID数据，支持重试"""
    if isinstance(id_info, tuple):
        id_value, alias = id_info
    else:
        id_value = id_info
        alias = id_value

    # 新增：检查是否为外部数据源
    if self.external_adapter and self.external_adapter.is_external_source(id_value):
        return self.external_adapter.fetch_external_data(id_value)

    # 原有的 newsnow 逻辑
    url = f"https://newsnow.busiyi.world/api/s?id={id_value}&latest"
    # ... 后续代码保持不变
```

---

## 配置文件修改

### `config/config.yaml` 

在 `platforms` 部分添加外部数据源：

```yaml
platforms:
  # 原有的平台
  - id: "toutiao"
    name: "今日头条"
  - id: "baidu"
    name: "百度热搜"
  - id: "weibo"
    name: "微博"
  - id: "zhihu"
    name: "知乎"
  
  # 新增外部数据源（可选）
  - id: "youtube-trending"
    name: "YouTube 热门视频"
  - id: "cnn-news"
    name: "CNN 新闻"
  - id: "hackernews"
    name: "Hacker News"
  - id: "newsapi-cnn-bbc"
    name: "新闻聚合(CNN/BBC)"
```

---

## 环境变量配置

创建或修改项目根目录的 `.env` 文件：

```bash
# YouTube API (可选)
YOUTUBE_API_KEY=AIza...your-key-here

# NewsAPI (可选)
NEWSAPI_KEY=abcd...your-key-here

# 代理设置 (可选)
PROXY_URL=http://proxy.example.com:8080
```

**或在命令行设置：**

```bash
export YOUTUBE_API_KEY="AIza..."
export NEWSAPI_KEY="abcd..."
python main.py
```

**或在 GitHub Actions 中设置：**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
      NEWSAPI_KEY: ${{ secrets.NEWSAPI_KEY }}
```

---

## 依赖项（无需额外安装）

外部数据源模块只使用标准库和已有的依赖：
- ✅ `requests` （已安装）
- ✅ `json` （标准库）
- ✅ `xml.etree.ElementTree` （标准库）

无需运行 `pip install ...`

---

## 完整代码示例

### 修改后的 `DataFetcher` 类（关键部分）

```python
from typing import Dict, List, Tuple, Optional, Union

class DataFetcher:
    """数据获取器"""

    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        
        # 初始化外部数据源适配器
        try:
            from sources.adapter import get_adapter
            self.external_adapter = get_adapter(proxy_url)
            print("✅ 外部数据源模块已加载")
        except Exception as e:
            self.external_adapter = None
            print(f"⚠️ 外部数据源初始化失败: {e}，仅使用 newsnow")

    def fetch_data(
        self,
        id_info: Union[str, Tuple[str, str]],
        max_retries: int = 2,
        min_retry_wait: int = 3,
        max_retry_wait: int = 5,
    ) -> Tuple[Optional[str], str, str]:
        """获取指定ID数据，支持重试"""
        if isinstance(id_info, tuple):
            id_value, alias = id_info
        else:
            id_value = id_info
            alias = id_value

        # 优先检查是否为外部数据源
        if self.external_adapter and self.external_adapter.is_external_source(id_value):
            print(f"正在从外部源获取 {id_value} 数据...")
            return self.external_adapter.fetch_external_data(id_value)

        # 使用 newsnow 获取数据（原有逻辑）
        url = f"https://newsnow.busiyi.world/api/s?id={id_value}&latest"

        proxies = None
        if self.proxy_url:
            proxies = {"http": self.proxy_url, "https": self.proxy_url}

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
        }

        retries = 0
        while retries <= max_retries:
            try:
                response = requests.get(
                    url, proxies=proxies, headers=headers, timeout=10
                )
                response.raise_for_status()

                data_text = response.text
                data_json = json.loads(data_text)

                status = data_json.get("status", "未知")
                if status not in ["success", "cache"]:
                    raise ValueError(f"响应状态异常: {status}")

                status_info = "最新数据" if status == "success" else "缓存数据"
                print(f"获取 {id_value} 成功（{status_info}）")
                return data_text, id_value, alias

            except Exception as e:
                retries += 1
                if retries <= max_retries:
                    base_wait = random.uniform(min_retry_wait, max_retry_wait)
                    additional_wait = (retries - 1) * random.uniform(1, 2)
                    wait_time = base_wait + additional_wait
                    print(f"请求 {id_value} 失败: {e}. {wait_time:.2f}秒后重试...")
                    time.sleep(wait_time)
                else:
                    print(f"请求 {id_value} 失败: {e}")
                    return None, id_value, alias
        return None, id_value, alias

    def crawl_websites(self, ids_list: List[Union[str, Tuple[str, str]]], request_interval: int = 1000) -> Tuple[Dict, Dict, List]:
        """爬取多个网站数据（支持混合 newsnow 和外部源）"""
        results = {}
        id_to_name = {}
        failed_ids = []

        for i, id_info in enumerate(ids_list):
            if isinstance(id_info, tuple):
                id_value, name = id_info
            else:
                id_value = id_info
                name = id_value

            id_to_name[id_value] = name
            response, _, _ = self.fetch_data(id_info)

            if response:
                try:
                    data = json.loads(response)
                    results[id_value] = {}
                    for index, item in enumerate(data.get("items", []), 1):
                        title = item.get("title")
                        if title is None or isinstance(title, float) or not str(title).strip():
                            continue
                        title = str(title).strip()
                        url = item.get("url", "")
                        mobile_url = item.get("mobileUrl", "")

                        if title in results[id_value]:
                            results[id_value][title]["ranks"].append(index)
                        else:
                            results[id_value][title] = {
                                "ranks": [index],
                                "url": url,
                                "mobileUrl": mobile_url,
                            }
                except Exception as e:
                    print(f"处理 {id_value} 数据出错: {e}")
                    failed_ids.append(id_value)
            else:
                failed_ids.append(id_value)

            if i < len(ids_list) - 1:
                actual_interval = request_interval + random.randint(-10, 20)
                actual_interval = max(50, actual_interval)
                time.sleep(actual_interval / 1000)

        print(f"成功: {list(results.keys())}, 失败: {failed_ids}")
        return results, id_to_name, failed_ids
```

---

## 测试

应用修改后，运行以下测试：

```bash
# 测试外部数据源是否正确加载
python -c "from sources.adapter import get_adapter; adapter = get_adapter(); print('支持的数据源:', adapter.get_available_sources())"

# 测试完整流程
python main.py
```

**预期输出：**
```
✅ YouTube 数据源已初始化
✅ CNN 数据源已初始化
✅ Hacker News 数据源已初始化
✅ 外部数据源模块已加载
正在爬取数据，请求间隔 1000 毫秒
当前监控平台: ['toutiao', 'baidu', 'youtube-trending', 'cnn-news', ...]
获取 toutiao 成功（最新数据）
正在从外部源获取 youtube-trending 数据...
✅ YouTube: 成功获取 50 条热门视频
成功: ['toutiao', 'baidu', 'youtube-trending', ...], 失败: []
```

---

## 回滚

如果需要禁用外部数据源，只需注释掉 `config.yaml` 中的外部平台配置：

```yaml
# - id: "youtube-trending"
#   name: "YouTube 热门视频"
# - id: "cnn-news"
#   name: "CNN 新闻"
```

系统会自动降级到仅使用 newsnow。

---

## 注意事项

1. ⚠️ **API Key 安全**：不要在代码中硬编码 API Key，使用环境变量
2. ⚠️ **配额限制**：某些 API（如 YouTube）有每日请求限制
3. ⚠️ **网络要求**：外部数据源需要国际网络连接
4. ✅ **错误恢复**：如果某个数据源失败，不会影响其他源

---

## 支持

详见 `EXTERNAL_SOURCES_GUIDE.md`

