# ⚡ 快速集成外部数据源（5分钟）

## 🎯 目标：添加 CNN + YouTube 到 TrendRadar

### 步骤 1️⃣：复制文件（30秒）

已为你准备好了以下文件，放在项目根目录下：

```
sources/
├── __init__.py
├── external_sources.py      # 核心实现
└── adapter.py               # 与 main.py 适配器
```

### 步骤 2️⃣：修改 main.py（2分钟）

**打开 `main.py`，找到第 471-476 行的 `DataFetcher.__init__`：**

❌ **原代码：**
```python
class DataFetcher:
    """数据获取器"""

    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
```

✅ **改为：**
```python
class DataFetcher:
    """数据获取器"""

    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        try:
            from sources.adapter import get_adapter
            self.external_adapter = get_adapter(proxy_url)
        except ImportError:
            self.external_adapter = None
```

---

**找到第 491 行的 `fetch_data` 方法：**

❌ **原代码：**
```python
    def fetch_data(self, ...):
        """获取指定ID数据，支持重试"""
        if isinstance(id_info, tuple):
            id_value, alias = id_info
        else:
            id_value = id_info
            alias = id_value

        url = f"https://newsnow.busiyi.world/api/s?id={id_value}&latest"
```

✅ **改为：**
```python
    def fetch_data(self, ...):
        """获取指定ID数据，支持重试"""
        if isinstance(id_info, tuple):
            id_value, alias = id_info
        else:
            id_value = id_info
            alias = id_value

        # 新增：检查外部数据源
        if self.external_adapter and self.external_adapter.is_external_source(id_value):
            return self.external_adapter.fetch_external_data(id_value)

        url = f"https://newsnow.busiyi.world/api/s?id={id_value}&latest"
```

### 步骤 3️⃣：修改配置（1分钟）

**编辑 `config/config.yaml`，在 `platforms` 部分添加：**

```yaml
platforms:
  # 原有平台...
  
  # 新增外部数据源
  - id: "youtube-trending"
    name: "YouTube 热门"
  - id: "cnn-news"
    name: "CNN"
```

### 步骤 4️⃣：（可选）设置 API Key

**如果要使用 YouTube，需要设置环境变量：**

```bash
export YOUTUBE_API_KEY="your-key-here"
```

**获取 YouTube API Key：**
1. 访问 https://console.cloud.google.com
2. 创建项目 → 启用 YouTube Data API v3
3. 创建 API 凭证 → 复制 API 密钥

**CNN 不需要 API Key** ✅

### 步骤 5️⃣：运行！

```bash
python main.py
```

**预期输出：**
```
✅ YouTube 数据源已初始化
✅ CNN 数据源已初始化
✅ Hacker News 数据源已初始化
✅ 外部数据源模块已加载
获取 youtube-trending 成功
获取 cnn-news 成功
```

---

## 📊 支持的数据源速查表

| 数据源 | 配置 ID | 需要 API? | 难度 | 描述 |
|--------|--------|---------|------|------|
| YouTube 热门 | `youtube-trending` | ✅ | ⭐⭐⭐ | 最新热门视频 |
| CNN 新闻 | `cnn-news` | ❌ | ⭐ | 最新新闻 |
| NewsAPI | `newsapi-cnn-bbc` | ✅ | ⭐⭐ | 多源聚合 |
| Hacker News | `hackernews` | ❌ | ⭐ | 技术讨论 |

---

## 🆘 快速排查

### ❌ 错误：`ModuleNotFoundError: No module named 'sources'`

**解决：** 确保 `sources/` 文件夹在项目根目录

```bash
ls -la sources/
# 应该显示: __init__.py, external_sources.py, adapter.py
```

### ❌ 错误：`YouTube 数据源已初始化 但获取失败`

**解决：** 检查 API Key

```bash
echo $YOUTUBE_API_KEY  # 应该显示你的 key
```

### ❌ 其他错误

**查看完整文档：** 见 `EXTERNAL_SOURCES_GUIDE.md`

---

## ✨ 完成！

现在你可以：
- ✅ 同时监控 YouTube、CNN、新闻源
- ✅ 混合 newsnow + 外部源
- ✅ 自动保存到 `output/` 目录
- ✅ 支持推送通知

---

## 📚 下一步

- 想了解更多？阅读 `EXTERNAL_SOURCES_GUIDE.md`
- 想自定义？阅读 `INTEGRATION_PATCH.md`
- 想添加更多源？见源代码的扩展说明

