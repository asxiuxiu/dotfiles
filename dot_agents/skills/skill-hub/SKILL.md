# Skill Hub

管理个人 skill 的同步与分发。将 user scope skills（`~/.agents/skills/`）用 chezmoi 纳入版本控制，实现跨电脑一键同步。

## 触发场景

- "skill hub"
- "同步 skills"
- "skills 管理"
- "skills push / pull"
- "skill 备份"
- "新电脑装 skills"

## 架构

| 位置 | 用途 | 同步方式 |
|------|------|----------|
| `~/.agents/skills/` (User scope) | 通用 skills，跨所有项目可用 | **chezmoi** → `dotfiles` 仓库 |
| `<vault>/.agents/skills/` (Project scope) | vault 专属 skills | 跟随 vault git 同步 |

## 环境信息

- chezmoi 本地仓库：`~/.local/share/chezmoi/`
- 远程仓库：`https://github.com/asxiuxiu/dotfiles.git`
- User scope skills 源目录：`dot_agents/skills/`（chezmoi 内部路径名）

## 子命令

### push（推送变更到远程）

将本地所有 user scope skills 的修改提交并推送到远程 dotfiles 仓库。

```bash
cd ~/.local/share/chezmoi
# 重新扫描并添加所有 skill 变更（幂等）
for dir in ~/.agents/skills/*/; do
    chezmoi add "$dir"
done
# 查看变更摘要
chezmoi git -- diff --stat --cached
chezmoi git -- add -A
chezmoi git -- commit -m "skills: sync $(date +%Y-%m-%d)"
chezmoi git -- push
```

> 若用户提供了 commit message，优先使用用户输入的消息。

### pull（拉取远程并应用）

从远程 dotfiles 仓库拉取最新的 skills 并应用到本地。

```bash
cd ~/.local/share/chezmoi
chezmoi git -- pull
chezmoi apply ~/.agents/skills/
```

应用前可先执行 `chezmoi diff ~/.agents/skills/` 确认变更。

### status（查看同步状态）

```bash
chezmoi status ~/.agents/skills/
chezmoi diff ~/.agents/skills/
chezmoi git -- -C ~/.local/share/chezmoi log --oneline -5 -- dot_agents/skills/
```

### list（列出所有 skills）

分别列出 user scope 和当前 vault 的 project scope skills。

```bash
echo "=== User Scope (~/.agents/skills/) ==="
ls ~/.agents/skills/
echo ""
echo "=== Project Scope (vault/.agents/skills/) ==="
ls D:/obsidian_lib/.agents/skills/ 2>/dev/null || echo "no project scope skills found"
```

### new（创建新 skill 骨架）

快速创建一个新 skill 目录和 `SKILL.md` 模板，并自动加入 chezmoi 管理。

用法：`new <skill-name>`

步骤：
1. `mkdir -p ~/.agents/skills/<skill-name>`
2. 写入 `SKILL.md` 模板（见下方）
3. `chezmoi add ~/.agents/skills/<skill-name>/`
4. 提示用户编辑 `~/.agents/skills/<skill-name>/SKILL.md`

**SKILL.md 最小模板**：

```markdown
# <Skill 名称>

## 触发场景

- "触发词1"
- "触发词2"

## 功能描述

简述这个 skill 解决什么问题。

## 子命令

### 命令1

步骤：
1. ...
2. ...

### 命令2

步骤：
1. ...
2. ...

## 环境信息

- 相关路径：...
- 依赖工具：...

## 注意事项

- ...
```

## 新电脑初始化流程

在一台全新电脑上恢复 skills：

```bash
# 1. 安装 chezmoi
winget install twpayne.chezmoi

# 2. 初始化并拉取 dotfiles
chezmoi init --apply https://github.com/asxiuxiu/dotfiles.git

# 3. 验证 skills 已恢复
ls ~/.agents/skills/
```

## 注意事项

### Project scope vs User scope

- 如果某个 skill **只在特定 vault 里用**（如 `cpp-practice-orchestrator`），放在 vault 的 `.agents/skills/` 里，跟随 vault git 走。
- 如果某个 skill **想在所有电脑/所有项目通用**（如 `git-sync`、`skill-hub`），放在 `~/.agents/skills/` 里，用 chezmoi 同步。

### 避免重复同步

不要通过 chezmoi 管理 `<vault>/.agents/skills/` 目录——这些由 vault 自己的 git 管理，否则会产生双重版本控制冲突。

### 大文件与二进制

skill 目录里尽量只放 markdown、yaml、json 等文本文件。如果 skill 需要附带大型二进制（如图片、模型），建议：
1. 将二进制放到外部存储（CDN、图床、网盘）
2. skill 里只保留下载链接和安装脚本
