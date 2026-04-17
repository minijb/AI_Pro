# Raw Sources — 源文档目录

> 归档后不可变。所有文件由 Claude 从 `_input/files/` 读取并处理。

## 目录结构

| 目录 | 用途 | 归档后 |
|------|------|--------|
| `_input/files/` | **摄入入口**，用户放入未分类源文件 | 处理后清空 |
| `_input/reports/` | **报告目录**，每次 ingest 报告输出 | 保留 |
| `articles/` | 网页文章（Web Clipper 抓取） | 不可变 |
| `papers/` | 论文 | 不可变 |
| `books/` | 书籍 | 不可变 |
| `videos/` | 视频 | 不可变 |
| `podcasts/` | 播客 | 不可变 |
| `notes/` | **个人随手笔记**（对话记录、灵感、速记） | 不可变 |
| `diary/` | 日记 | 不可变 |
| `images/assets/` | 图片资产 | 不可变 |

## 分类说明

| 分类 | 内容示例 |
|------|---------|
| `articles/` | 网页文章、博客、技术帖子 |
| `papers/` | 学术论文、技术报告 |
| `books/` | 书籍章节、读书笔记 |
| `videos/` | 视频字幕、视频笔记 |
| `podcasts/` | 播客转录、播客笔记 |
| `notes/` | **个人随手笔记**：对话记录、项目灵感、学习速记、问题备忘 |
| `diary/` | 日记、每日总结 |
| `images/assets/` | 图片、截图、图表 |

> [!tip] notes/ 的用途
> `notes/` 是你个人的随手笔记仓库。任何不在上述分类中的内容——对话片段、项目灵感、问题备忘、学习速记——都可以存放在这里。ingest 后会整理到对应的 wiki 分类。

## 使用流程

1. 将新文件放入 `_input/files/`
2. 对 Claude 说「处理这个源」触发 ingest
3. Claude 会：
   - 分析文件类型并移动到对应分类
   - 创建 wiki 页面
   - 生成报告到 `_input/reports/`
   - 更新所有索引和 Memory

## 绝对规则

- **从不直接修改归档目录中的文件**
- **从不从归档目录中读取源内容**（只从 `_input/files/` 读取）
- **单文件摄入**：一次处理一个文件

---

> [!tip] 提示
> 本目录基于 CLAUDE.md 的 LLM Wiki 模式设计。详见 `.claudian/system-prompt.md`。
