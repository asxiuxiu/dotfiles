---
name: vault-context
description: 当用户请求参考 Obsidian 知识库、使用 vault 中的笔记、或在 vibe coding 时需要引入 D:\asxiuxiu_obsidian_repo 中的架构/源码分析知识时，读取此 skill 并主动搜索/读取相关笔记。
---

# Vault 上下文注入指南

## 仓库位置

用户的 Obsidian 知识库（Vault）根目录固定位于：

```
D:\asxiuxiu_obsidian_repo
```

Vault 名称（用于 obsidian-cli）为：`asxiuxiu_obsidian_repo`

## 目录结构

| 目录 | 用途 | 常见内容 |
|------|------|----------|
| `Notes/计算机图形学/` | 渲染、图形学基础 | 渲染管线、光照模型、PBR、延迟渲染等 |
| `Notes/游戏引擎/` | 引擎架构通用知识 | ECS、反射系统、内存管理、资源管线等 |
| `Notes/C++编程/` | C++ 语言与工程实践 | 模板元编程、并发、构建系统、设计模式等 |
| `Notes/数学基础/` | 图形/物理数学 | 线性代数、四元数、碰撞检测、数值方法等 |
| `Notes/人工智能/` | AI 算法与系统 | 行为树、状态机、寻路、机器学习基础等 |
| `Notes/构建系统/` | CMake、编译链接 | CMake 最佳实践、编译器原理等 |
| `Notes/学习计划/` | 学习路线图与总结 | 主题清单、进度追踪等 |
| `Notes/索引/` | MOC、总索引 | 各分类的 `索引.md` 入口 |
| `Game/` | 保密源码分析笔记 | chaos 引擎、proven_ground、wolfgang 等源码解析 |
| `workspace/` | 代码实践、示例项目 | C++ 实验代码、CMake 模板等 |
| `Assets/` | 图片资源 | games/、graphics/、math/、ai/ 分类图 |

## 主动行为（无需用户手动复制粘贴）

当用户的发言涉及以下任一意图时，**你必须主动读取知识库中的相关笔记**，而不是等待用户把内容贴给你：

- "参考我知识库里的 xxx"
- "根据我笔记里的 xxx 方案来设计"
- "vibe coding 这个模块，和知识库里的 xxx 对照一下"
- "帮我看看这个实现和笔记里记录的有什么区别"
- "按照 vault 里总结的模式来写"

## 搜索策略：优先使用 obsidian-cli

当 Obsidian 应用正在运行时，**优先使用 obsidian-cli 进行搜索**，因为它能利用 Obsidian 的全文索引、frontmatter 和 wikilink 解析，效果通常优于原生 Grep。

### obsidian-cli 搜索命令

```powershell
# 基础搜索：返回匹配的文件路径列表（推荐先用这个快速定位）
obsidian vault="asxiuxiu_obsidian_repo" search query="渲染管线" limit=10

# 带上下文的搜索：返回匹配行及内容片段（想快速确认相关性时用）
obsidian vault="asxiuxiu_obsidian_repo" search:context query="ECS" limit=10

# 限定在 Game/ 目录下搜索
obsidian vault="asxiuxiu_obsidian_repo" search query="反射系统" path="Game" limit=10

# 读取找到的笔记（通过路径，无需扩展名）
obsidian vault="asxiuxiu_obsidian_repo" read path="Notes/游戏引擎/ECS-源码解析"
```

### 使用 obsidian-cli 的完整流程

1. **执行搜索**：用 `obsidian search` 或 `obsidian search:context` 查找相关文件。
2. **判断相关性**：根据返回的文件名和上下文片段，挑选 1-3 篇最相关的笔记。
3. **读取内容**：用 `obsidian read path="..."` 读取选中笔记的完整内容。
4. **整合应用**：提取核心概念、设计模式、代码示例，应用到用户的当前任务中。

### obsidian-cli 不可用时的回退方案

如果 obsidian-cli 返回错误（如 Obsidian 未运行、命令不存在），立即回退到以下方式：

```powershell
# 用 Grep 在知识库中搜索关键词
Grep(pattern: "渲染管线", path: "D:\\asxiuxiu_obsidian_repo\\Notes\\计算机图形学")

# 用 Glob 列出索引文件
Glob(pattern: "Notes/*/索引.md", directory: "D:\\asxiuxiu_obsidian_repo")

# 用 ReadFile 直接读取（支持绝对路径）
ReadFile(path: "D:\\asxiuxiu_obsidian_repo\\Notes\\游戏引擎\\ECS-源码解析.md")
```

## 如何查找笔记（详细步骤）

1. **确定主题范围**：根据用户描述，判断应该去 `Notes/` 下的哪个子目录，还是去 `Game/` 目录。
2. **快速定位**：
   - 首选 `obsidian search`（如果 Obsidian 在运行）。
   - 次选 `Grep`/`Glob`（直接用绝对路径）。
3. **读取内容**：并行读取最相关的 1-3 篇笔记。
4. **整合上下文**：将笔记中的核心概念、设计模式、代码示例提取出来，应用到用户当前的 vibe coding 任务中。

## 关于 /add-dir

虽然你可以直接读取绝对路径，但如果用户准备进行**多轮深度 vibe coding**，频繁往返于知识库和项目代码之间，建议提示用户：

> 为了方便后续多轮对话中自动搜索，你可以执行 `/add-dir D:\asxiuxiu_obsidian_repo` 把知识库挂载到当前工作区。

**不要强制要求用户执行此命令**，只在会话明显会长期依赖知识库时提出建议。

## 引用规范

- 笔记中的 Wikilink（如 `[[索引|xxx索引]]`）在回答里可以直接用文字引用。
- 如果笔记里有代码示例，直接提取并说明其适用场景。
- 遇到 `Game/` 目录下的保密源码分析，**只提取通用工程原理**，不透露项目专属的业务逻辑或敏感数据。
