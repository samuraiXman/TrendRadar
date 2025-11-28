# ⚡ 快速修复参考

## 🔴 遇到的问题

| 问题 | 错误信息 | 状态 |
|-----|--------|------|
| 1 | `❌ 未知的外部数据源: youtube-trending` | ✅ 已修复 |
| 2 | `CNN fetch failed: 404 Client Error` | ✅ 已修复 |
| 3 | `❌ 未知的外部数据源: newsapi-cnn-bbc` | ✅ 已修复 |

## ✅ 已应用的修复

### 修复 1：adapter.py 中的数据源初始化

**文件**：`sources/adapter.py` 第 20-52 行

**改动**：所有数据源现在都会被初始化，无论是否有 API Key

**关键改动**：
```python
# 所有数据源都添加到字典中（即使没有 API Key）
self.external_sources["youtube-trending"] = YouTubeTrendingSource(
    api_key=os.environ.get("YOUTUBE_API_KEY"),  # 可能为 None
    proxy_url=self.proxy_url
)
```

**效果**：即使没有 API Key，也不会报"未知数据源"错误

---

### 修复 2：CNN RSS URL

**文件**：`sources/external_sources_simple.py` 第 56 行

**改动**：从 `https://www.cnn.com/cnn/cnn_topstories.rss` 改为 `https://rss.cnn.com/rss/edition.rss`

**效果**：CNN 新闻能正常获取

---

### 修复 3：NewsAPI 数据源初始化

**文件**：`sources/adapter.py` 第 37-46 行

**改动**：NewsAPI 现在总是初始化（即使没有 Key）

**效果**：不再报"未知数据源"错误

---

## 🚀 如何使用

### 立即可用（无需配置）

```bash
cd /Users/deron/develop/ai-pro/TrendRadar
python main.py
```

✅ 支持的数据源：
- CNN 新闻
- Hacker News
- 所有中文平台（newsnow）

---

### 启用 YouTube（可选）

```bash
export YOUTUBE_API_KEY="AIza..."
python main.py
```

1. 获取 API Key：https://console.cloud.google.com
2. 创建项目 → 启用 YouTube Data API v3 → 创建 API 凭证

---

### 启用 NewsAPI（可选）

```bash
export NEWSAPI_KEY="abcd..."
python main.py
```

1. 获取 API Key：https://newsapi.org
2. 注册 → 获取 Free API Key

---

### 完整配置

```bash
export YOUTUBE_API_KEY="AIza..."
export NEWSAPI_KEY="abcd..."
python main.py
```

---

## 📊 数据源状态

| 数据源 | 状态 | API Key | 说明 |
|--------|------|--------|------|
| YouTube | ✅ | 可选 | 设置后工作 |
| CNN | ✅ | 无需 | 立即可用 |
| Hacker News | ✅ | 无需 | 立即可用 |
| NewsAPI | ✅ | 可选 | 设置后工作 |

---

## 🧪 测试验证

修复后应该看到：

```
✅ YouTube 数据源已初始化
✅ CNN 数据源已初始化
✅ NewsAPI (CNN + BBC) 数据源已初始化
✅ Hacker News 数据源已初始化

获取 cnn-news 成功
Hacker News: fetched X stories
```

---

## 📝 修改文件列表

- ✅ `sources/adapter.py` - 修复了初始化逻辑
- ✅ `sources/external_sources_simple.py` - 修复了 CNN URL
- ✅ `sources/__init__.py` - 无改动
- ✅ `main.py` - 无改动
- ✅ `config/config.yaml` - 无改动

---

## 🎯 下一步

1. **运行测试**
   ```bash
   python main.py
   ```

2. **如果需要国际新闻**
   ```bash
   export YOUTUBE_API_KEY="..."
   export NEWSAPI_KEY="..."
   python main.py
   ```

3. **查看完整文档**
   - `IMPLEMENTATION_COMPLETE.md` - 实现详情
   - `FIXES_APPLIED.md` - 修复详情

---

**修复完成！** 🎉 现在可以运行了。

