# 🌐 外部数据源集成指南

本指南说明如何在 TrendRadar 中集成 CNN、YouTube 等外部数据源。

## 📋 目录

1. [快速开始](#快速开始)
2. [支持的数据源](#支持的数据源)
3. [配置方式](#配置方式)
4. [获取 API Key](#获取-api-key)
5. [故障排除](#故障排除)

---

## 🚀 快速开始

### 第一步：选择数据源

TrendRadar 目前支持以下外部数据源：

| 数据源 | 需要 API | 配置参数 | 使用难度 |
|--------|---------|---------|---------|
| **YouTube 热门视频** | ✅ 是 | `YOUTUBE_API_KEY` | ⭐⭐⭐ |
| **CNN 新闻** | ❌ 否 | 无 | ⭐ |
| **NewsAPI (通用)** | ✅ 是 | `NEWSAPI_KEY` | ⭐⭐ |
| **Hacker News** | ❌ 否 | 无 | ⭐ |

### 第二步：修改 `main.py`

在 `main.py` 的 `DataFetcher` 类中添加支持。找到以下位置：

```python
# 约在第471行
class DataFetcher:
    """数据获取器"""

    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        # 添加以下代码
        from sources.adapter import get_adapter
        self.external_adapter = get_adapter(proxy_url)
```

然后修改 `fetch_data` 方法：

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
    if self.external_adapter.is_external_source(id_value):
        return self.external_adapter.fetch_external_data(id_value)

    # 原有的 newsnow 逻辑...
    url = f"https://newsnow.busiyi.world/api/s?id={id_value}&latest"
    # ... 后续代码保持不变
```

### 第三步：修改配置文件

编辑 `config/config.yaml`，在 `platforms` 段添加外部数据源：

```yaml
platforms:
  # 原有的平台
  - id: "toutiao"
    name: "今日头条"
  - id: "baidu"
    name: "百度热搜"
  
  # 添加新的外部数据源
  - id: "youtube-trending"
    name: "YouTube 热门视频"
  - id: "cnn-news"
    name: "CNN 新闻"
  - id: "hackernews"
    name: "Hacker News"
  - id: "newsapi-cnn-bbc"
    name: "新闻聚合(CNN/BBC)"
```

### 第四步：设置环境变量

根据选择的数据源，设置相应的 API Key：

```bash
# 如果使用 YouTube
export YOUTUBE_API_KEY="your-youtube-api-key"

# 如果使用 NewsAPI
export NEWSAPI_KEY="your-newsapi-key"
```

或在 `.env` 文件中设置（如果项目支持）。

### 第五步：运行

```bash
python main.py
```

---

## 📊 支持的数据源

### 1. **YouTube 热门视频**

获取 YouTube 平台最新热门视频。

**配置示例：**
```yaml
- id: "youtube-trending"
  name: "YouTube 热门"
```

**需要的环境变量：**
```bash
YOUTUBE_API_KEY=your-key-here
```

**数据示例：**
```
视频标题 | 观看次数 | 点赞数 | 评论数
How to Learn Python | 1.5M | 45K | 2.3K
Breaking News | 500K | 12K | 1.2K
```

**配置 API Key：** 见 [获取 YouTube API Key](#获取-youtube-api-key)

---

### 2. **CNN 新闻**

获取 CNN 最新新闻头条。

**配置示例：**
```yaml
- id: "cnn-news"
  name: "CNN"
```

**无需 API Key** ✅

**数据示例：**
```
Breaking: Congress passes new legislation
Markets rally on positive earnings
International tensions escalate
```

**优点：**
- ✅ 无需 API Key
- ✅ 实时新闻
- ✅ 可靠性高

---

### 3. **NewsAPI 聚合源**

通过 NewsAPI 获取多个新闻源（CNN、BBC、Reuters 等）。

**配置示例：**
```yaml
- id: "newsapi-cnn-bbc"
  name: "新闻聚合(CNN/BBC)"
```

**需要的环境变量：**
```bash
NEWSAPI_KEY=your-key-here
```

**支持的源代码：**
```
- cnn
- bbc-news
- bloomberg
- reuters
- new-york-times
- the-guardian
- financial-times
- ... (50+ 个源)
```

**配置 API Key：** 见 [获取 NewsAPI Key](#获取-newsapi-key)

---

### 4. **Hacker News**

获取 Hacker News 热门讨论。

**配置示例：**
```yaml
- id: "hackernews"
  name: "Hacker News"
```

**无需 API Key** ✅

**数据示例：**
```
Show HN: Project X - New framework
The future of AI
Why I left FAANG
```

**特点：**
- ✅ 无需认证
- ✅ 技术社区讨论
- ✅ 有 API 限流（已处理）

---

## 🔧 配置方式

### 方式 1：环境变量（推荐）

**本地开发：**
```bash
export YOUTUBE_API_KEY="AIza..."
export NEWSAPI_KEY="abcd..."
python main.py
```

**GitHub Actions：**
在 `.github/workflows/xxx.yml` 中设置：
```yaml
env:
  YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
  NEWSAPI_KEY: ${{ secrets.NEWSAPI_KEY }}
```

### 方式 2：Docker 环境变量

```bash
docker run -e YOUTUBE_API_KEY="..." -e NEWSAPI_KEY="..." trendradar:latest
```

### 方式 3：Docker Compose

```yaml
services:
  trendradar:
    image: trendradar:latest
    environment:
      YOUTUBE_API_KEY: ${YOUTUBE_API_KEY}
      NEWSAPI_KEY: ${NEWSAPI_KEY}
```

---

## 🔑 获取 API Key

### 获取 YouTube API Key

1. 访问 [Google Cloud Console](https://console.cloud.google.com)
2. 创建新项目或选择现有项目
3. 启用 **YouTube Data API v3**
4. 创建 **API 凭证** → **API 密钥**
5. 复制生成的 API Key

**费用：** 免费（有配额限制：每日 10,000 个单位）

---

### 获取 NewsAPI Key

1. 访问 [NewsAPI.org](https://newsapi.org)
2. 注册账户
3. 获取 API Key
4. 选择免费计划或付费计划

**费用：** 免费版 + 500 请求/天

---

## 🛠️ 故障排除

### 问题 1：API Key 无效

**症状：**
```
❌ YouTube 数据获取失败: 401 Unauthorized
```

**解决：**
- 检查 API Key 是否正确
- 确认 API 已启用（在 Google Cloud Console）
- 检查配额是否已用完

### 问题 2：网络超时

**症状：**
```
❌ CNN 数据获取失败: Connection timeout
```

**解决：**
- 检查网络连接
- 配置代理（如需要）
- 增加超时时间（在 `external_sources.py` 中修改 `timeout=15`）

### 问题 3：数据源未发现

**症状：**
```
❌ 未知的外部数据源: youtube-trending
```

**解决：**
- 确保在 `config.yaml` 中正确配置了平台
- 检查拼写是否正确
- 运行 `python -c "from sources.adapter import get_adapter; print(get_adapter().get_available_sources())"`

### 问题 4：API 请求超限

**症状：**
```
❌ API 返回错误: Daily limit exceeded
```

**解决：**
- 等待 24 小时后重试
- 升级到付费计划
- 减少请求频率（修改 `config.yaml` 中的 `request_interval`）

---

## 📈 性能优化

### 1. 缓存数据

外部 API 响应已自动缓存 15 分钟，无需重复配置。

### 2. 批量请求

系统自动处理请求间隔，避免触发速率限制。

### 3. 错误恢复

如果某个数据源失败，系统会继续处理其他源，不会中断。

---

## 🚀 高级用法

### 自定义数据源

如果需要添加其他数据源（如 Reddit、Product Hunt 等），可以扩展 `external_sources.py`：

```python
class RedditSource(ExternalDataSource):
    """Reddit 热门帖子"""
    
    def __init__(self, proxy_url: Optional[str] = None):
        super().__init__(proxy_url)
        self.base_url = "https://www.reddit.com/r/all"
    
    def fetch_data(self) -> Dict:
        # 实现获取逻辑
        pass
```

然后在 `adapter.py` 的 `_initialize_sources` 中注册：

```python
self.external_sources["reddit-hot"] = RedditSource(proxy_url=self.proxy_url)
```

最后在 `config.yaml` 中添加：

```yaml
- id: "reddit-hot"
  name: "Reddit 热门"
```

---

## 📝 更新日志

- **v1.0** (2025-01-01): 初始版本，支持 YouTube、CNN、NewsAPI、Hacker News
- 计划支持：Reddit、Product Hunt、Twitter、Medium 等

---

## ❓ 常见问题

**Q: 可以同时使用 newsnow 和外部数据源吗？**
A: 是的，系统会自动检测数据源类型，无缝集成。

**Q: 外部数据源的数据会保存吗？**
A: 是的，与 newsnow 数据格式相同，会保存到 `output/` 目录。

**Q: 性能如何？**
A: 外部 API 请求通常需要 1-5 秒，已优化处理速率限制。

**Q: 如何只使用外部数据源？**
A: 在 `config.yaml` 的 `platforms` 中只配置外部源即可。

---

## 📞 支持

如有问题，请：
1. 检查本指南的 [故障排除](#故障排除) 部分
2. 查看 `logs/` 目录中的错误日志
3. 提交 Issue

---

**祝使用愉快！🎉**

