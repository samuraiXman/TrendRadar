# 🌐 TrendRadar 外部数据源集成

> 🎯 **目标**：将 CNN、YouTube 等国际数据源集成到 TrendRadar
>
> ⏱️ **耗时**：5-10 分钟  
> 💰 **成本**：￥0（全部免费）  
> 📊 **覆盖**：中文 + 国际新闻

---

## 📚 文档导航

| 文档 | 用途 | 读者 |
|------|------|------|
| **QUICK_START_EXTERNAL_SOURCES.md** | 🚀 5 分钟快速集成 | 想快速上手的用户 |
| **EXTERNAL_SOURCES_GUIDE.md** | 📖 完整配置指南 | 想深入了解的用户 |
| **INTEGRATION_PATCH.md** | 🔧 代码修改详解 | 想看具体代码的用户 |
| **DATA_SOURCES_COMPARISON.md** | 📊 方案对比分析 | 想选择最优方案的用户 |

---

## 🎯 快速答案

### 问：能添加 CNN 和 YouTube 吗？

**答：可以！** ✅

### 问：需要改代码吗？

**答：是的，但很简单。** 仅需改 2 处（8 行代码）

### 问：需要钱吗？

**答：不需要！** 全部免费 API

### 问：难吗？

**答：不难。** 5-10 分钟完成

---

## 🚀 三种开始方式

### 方式 1：我很着急（3 分钟）

👉 **阅读：** `QUICK_START_EXTERNAL_SOURCES.md`

按照步骤复制文件、改代码、改配置、运行。

---

### 方式 2：我想充分理解（20 分钟）

👉 **按顺序阅读：**
1. `QUICK_START_EXTERNAL_SOURCES.md` - 快速了解
2. `EXTERNAL_SOURCES_GUIDE.md` - 详细说明
3. `INTEGRATION_PATCH.md` - 代码详解

---

### 方式 3：我想看方案对比（15 分钟）

👉 **阅读：** `DATA_SOURCES_COMPARISON.md`

对比所有方案的优缺点，选择最适合的。

---

## 📦 包含内容

```
sources/                          # 新增文件夹
├── __init__.py                   # 模块初始化
├── external_sources.py           # 核心实现（350 行）
│   ├── YouTubeTrendingSource      # YouTube 视频
│   ├── CNNNewsSource              # CNN 新闻
│   ├── NewsAPISource              # 多源聚合
│   └── HackerNewsSource           # 技术讨论
└── adapter.py                    # 与 main.py 适配器（100 行）

文档/
├── QUICK_START_EXTERNAL_SOURCES.md      # 5 分钟快速开始
├── EXTERNAL_SOURCES_GUIDE.md            # 完整配置指南
├── INTEGRATION_PATCH.md                 # 代码修改说明
├── DATA_SOURCES_COMPARISON.md           # 方案对比
└── EXTERNAL_SOURCES_README.md           # 本文件

需要修改/
├── main.py                       # 2 处修改（8 行代码）
└── config/config.yaml            # 添加新平台配置
```

---

## 🎬 快速演示

### 修改前

```
config/config.yaml
platforms:
  - id: "toutiao"
  - id: "weibo"
  - id: "baidu"
```

只有中文平台 ❌

### 修改后

```
config/config.yaml
platforms:
  - id: "toutiao"
  - id: "weibo"
  - id: "baidu"
  - id: "youtube-trending"      # 新增
  - id: "cnn-news"              # 新增
  - id: "hackernews"            # 新增
```

覆盖中文 + 国际新闻 ✅

---

## 📊 支持的数据源

### 🎥 YouTube 热门视频
```
视频标题 | 观看次数 | 点赞数 | 评论数
─────────────────────────────────
"How to..." | 1.5M | 45K | 2.3K
"Breaking..." | 500K | 12K | 1.2K
```

**配置：** `youtube-trending`  
**需要：** `YOUTUBE_API_KEY`  
**成本：** 免费（10K 单位/天）

---

### 📰 CNN 新闻
```
新闻标题 | 来源 | 发布时间
─────────────────────
"Congress passes..." | CNN | 2 小时前
"Markets rally..." | CNN | 1 小时前
```

**配置：** `cnn-news`  
**需要：** 无（RSS）  
**成本：** 免费

---

### 🌍 新闻聚合（NewsAPI）
支持 70+ 国际新闻源：
- CNN, BBC News, Reuters
- Bloomberg, Financial Times
- The Guardian, Associated Press
- ... 还有 60+ 个

**配置：** `newsapi-cnn-bbc`  
**需要：** `NEWSAPI_KEY`  
**成本：** 免费（500 请求/天）

---

### 💻 Hacker News（技术讨论）
```
讨论标题 | 热度 | 评论数
─────────────────────
"Show HN: ..." | 1.2K | 245
"Why I left..." | 956 | 123
```

**配置：** `hackernews`  
**需要：** 无（公开 API）  
**成本：** 免费（无限制）

---

## 🔧 集成难度

### 技术要求

- ✅ Python 基础
- ✅ 文本编辑器
- ✅ 会改配置文件
- ❌ 不需要深入编程知识

### 代码修改

- **文件数**：2 个（main.py, config.yaml）
- **修改行数**：8 行代码（都是复制粘贴）
- **创建文件**：3 个 Python 文件（已准备好）

### 难度评分

```
复制文件：⭐ 极简单
修改代码：⭐ 极简单
修改配置：⭐ 极简单
获取 API：⭐⭐ 简单
故障排查：⭐⭐ 简单

总难度：⭐ 极简单
```

---

## ✨ 集成后的效果

### 运行效果

```bash
$ python main.py

✅ YouTube 数据源已初始化
✅ CNN 数据源已初始化
✅ Hacker News 数据源已初始化
✅ NewsAPI 数据源已初始化
✅ 外部数据源模块已加载

正在爬取数据...
获取 toutiao 成功 （最新数据）
获取 youtube-trending 成功 （50 条视频）
获取 cnn-news 成功 （30 条新闻）
获取 hackernews 成功 （20 条讨论）

生成报告...
✅ HTML 报告: output/2025年01月28日/html/当日汇总.html
```

### 报告内容

原来的报告：
```
【当日热点统计】
AI | 12 条
手机 | 8 条
...
```

集成后的报告：
```
【当日热点统计】
AI | 20 条 ✨（原 12 条来自头条/微博 + 新增 8 条来自 YouTube/CNN）
手机 | 15 条（原 8 条 + 新增 7 条）
...

其中：
- 头条/微博/知乎：中文热点
- YouTube：热门视频
- CNN/NewsAPI：国际新闻
- Hacker News：技术讨论
```

---

## 🎓 学习路径

### 适合新手

```
1. 阅读 QUICK_START_EXTERNAL_SOURCES.md (5 min)
2. 按步骤操作 (5 min)
3. 运行测试 (2 min)
4. ✅ 完成！
```

总耗时：12 分钟

### 适合进阶用户

```
1. 阅读 DATA_SOURCES_COMPARISON.md (10 min)
2. 阅读 INTEGRATION_PATCH.md (10 min)
3. 审查 sources/external_sources.py (10 min)
4. 自定义配置 (10 min)
5. ✅ 完成！
```

总耗时：40 分钟

---

## 💡 常见问题快速答案

**Q: 会影响现有的 newsnow 功能吗？**  
A: 完全不会。新旧源完全兼容，和平共存。

**Q: 如果某个 API 挂掉怎么办？**  
A: 系统自动跳过，继续处理其他源。

**Q: 数据会重复吗？**  
A: 不会。系统自动去重。

**Q: 用多少个数据源会拖累性能？**  
A: 不会。系统并行处理，总耗时 5-10 秒。

**Q: 能自定义添加更多源吗？**  
A: 可以。代码设计支持扩展。

---

## 🚀 立即开始

### 1️⃣ 5 分钟快速版（推荐 ⭐）

```
👉 打开: QUICK_START_EXTERNAL_SOURCES.md
按照 5 个步骤操作
```

### 2️⃣ 完整学习版

```
👉 打开: EXTERNAL_SOURCES_GUIDE.md
详细了解每个配置选项
```

### 3️⃣ 方案选择版

```
👉 打开: DATA_SOURCES_COMPARISON.md
对比不同方案，选择最优
```

---

## 📞 需要帮助？

### 快速排查

| 问题 | 解决方案 |
|------|--------|
| 找不到 `sources/` 文件夹 | 见 QUICK_START（步骤 1） |
| 不知道怎么改 main.py | 见 INTEGRATION_PATCH（第 1-2 步） |
| API Key 获取失败 | 见 EXTERNAL_SOURCES_GUIDE（获取 API Key 部分） |
| 运行报错 | 见 EXTERNAL_SOURCES_GUIDE（故障排除） |

### 详细文档

- 所有配置选项：`EXTERNAL_SOURCES_GUIDE.md`
- 所有错误排查：`EXTERNAL_SOURCES_GUIDE.md` - 故障排除部分
- 代码细节：`INTEGRATION_PATCH.md`
- 源代码：`sources/external_sources.py`

---

## 📈 后续计划

### 已实现 ✅

- [x] YouTube 热门视频
- [x] CNN 新闻
- [x] NewsAPI 聚合源
- [x] Hacker News
- [x] 无缝集成到 main.py
- [x] 自动格式转换
- [x] 错误恢复机制

### 计划支持 📋

- [ ] Reddit 热门帖子
- [ ] Product Hunt
- [ ] Twitter 热门话题
- [ ] Medium 精选文章
- [ ] RSS 自定义源
- [ ] 数据库存储（目前为文件）

### 欢迎贡献 🤝

有想法？欢迎提交 Pull Request！

---

## 📄 许可证

与 TrendRadar 保持一致

---

## 🎉 开始集成吧！

选择你的方式：

- ⚡ **快速版**：[QUICK_START_EXTERNAL_SOURCES.md](./QUICK_START_EXTERNAL_SOURCES.md)
- 📖 **完整版**：[EXTERNAL_SOURCES_GUIDE.md](./EXTERNAL_SOURCES_GUIDE.md)
- 🔧 **代码版**：[INTEGRATION_PATCH.md](./INTEGRATION_PATCH.md)
- 📊 **对比版**：[DATA_SOURCES_COMPARISON.md](./DATA_SOURCES_COMPARISON.md)

**祝你使用愉快！** 🚀

