---
name: dotfiles-sync
description: "管理个人 dotfiles（skills、Zed 配置、clang-format 等）的 chezmoi 同步与分发。当用户说 dotfiles、同步配置、push/pull 设置、备份个人配置、新电脑恢复配置、同步 skills、同步 zed 配置时触发。"
---

# Dotfiles Sync

管理个人 dotfiles（skills、Zed 配置、clang-format 等）的 chezmoi 同步与分发。

## 触发场景

- "dotfiles"
- "同步配置"
- "push 设置"
- "pull 配置"
- "备份个人配置"
- "新电脑恢复配置"
- "同步 skills"
- "skills 管理"
- "skills push / pull"
- "skill 备份"
- "同步 zed 配置"
- "push zed 设置"
- "pull zed 配置"
- "zed chezmoi"

## 管理的资产

| 资产 | 本地路径 | chezmoi 源路径 | 说明 |
|------|----------|----------------|------|
| User scope skills | `~/.agents/skills/` | `dot_agents/skills/` | 通用 skills，跨所有项目可用 |
| Zed 配置 | `~/AppData/Roaming/Zed/` | `AppData/Roaming/Zed/` | 编辑器配置 |
| clang-format | `~/.clang-format` | `dot_clang-format` | C++ 格式化全局配置 |

**Project scope skills**（`<vault>/.agents/skills/`）跟随 vault git 同步，不由 chezmoi 管理。

## 环境信息

- chezmoi 本地仓库：`~/.local/share/chezmoi/`
- 远程仓库：`https://github.com/asxiuxiu/dotfiles.git`

## 子命令

### push（推送所有变更到远程）

将本地所有受管资产（skills、Zed、clang-format）的修改一次性提交并推送到远程。

```bash
cd ~/.local/share/chezmoi

# Skills
for dir in ~/.agents/skills/*/; do
    chezmoi add "$dir"
done

# Zed
chezmoi add ~/AppData/Roaming/Zed/settings.json
chezmoi add ~/AppData/Roaming/Zed/keymap.json
# 如有 themes/、tasks.json、snippets/，一并添加

# clang-format
chezmoi add ~/.clang-format

# 查看变更摘要
chezmoi git -- diff --stat

# 提交推送
chezmoi git -- add -A
chezmoi git -- commit -m "dotfiles: sync $(date +%Y-%m-%d)"
chezmoi git -- push
```

> 若用户提供了 commit message，优先使用用户输入的消息。

### pull（拉取远程并应用到本地）

从远程 dotfiles 仓库拉取最新配置并全部应用。

```bash
cd ~/.local/share/chezmoi
chezmoi git -- pull
chezmoi apply
```

应用前可先执行 `chezmoi diff` 确认变更内容，避免覆盖本地未备份的修改。

### status（查看同步状态）

```bash
chezmoi status
chezmoi diff
chezmoi git -- log --oneline -5
```

查看特定资产的差异：
```bash
# Zed
chezmoi diff ~/AppData/Roaming/Zed/

# Skills
chezmoi diff ~/.agents/skills/

# clang-format
chezmoi diff ~/.clang-format
```

### list（列出所有管理的资产）

```bash
echo "=== Skills (~/.agents/skills/) ==="
ls ~/.agents/skills/
echo ""
echo "=== Zed (~/AppData/Roaming/Zed/) ==="
ls ~/AppData/Roaming/Zed/ | grep -E 'settings|keymap|tasks|themes|snippets' || true
echo ""
echo "=== clang-format ==="
ls ~/.clang-format 2>/dev/null && echo "~/.clang-format" || echo "not found"
```

### new（创建新 skill 骨架）

快速创建一个新 skill 目录和 `SKILL.md` 模板，并自动加入 chezmoi 管理。

用法：`new <skill-name>`

步骤：
1. `mkdir -p ~/.agents/skills/<skill-name>`
2. 写入 `SKILL.md` 模板
3. `chezmoi add ~/.agents/skills/<skill-name>/`
4. 提示用户编辑内容

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

## 环境信息

- 相关路径：...
- 依赖工具：...
```

## 新电脑初始化流程

在一台全新电脑上恢复所有个人配置：

```bash
# 1. 安装 chezmoi
winget install twpayne.chezmoi

# 2. 初始化并拉取 dotfiles
chezmoi init --apply https://github.com/asxiuxiu/dotfiles.git

# 3. 验证已恢复
ls ~/.agents/skills/
ls ~/AppData/Roaming/Zed/
ls ~/.clang-format
```

## 注意事项

### Project scope vs User scope

- 如果某个 skill **只在特定 vault 里用**，放在 vault 的 `.agents/skills/` 里，跟随 vault git 走。
- 如果某个 skill **想在所有电脑/所有项目通用**，放在 `~/.agents/skills/` 里，用 chezmoi 同步。

### 避免重复同步

不要通过 chezmoi 管理 `<vault>/.agents/skills/` 目录——这些由 vault 自己的 git 管理，否则会产生双重版本控制冲突。

### 合并冲突

如果本地和远程同时修改了同一文件，`chezmoi git -- pull` 会产生冲突。此时需要：
1. 进入 `~/.local/share/chezmoi` 目录
2. 手动解决冲突文件
3. `chezmoi git -- add -A`
4. `chezmoi git -- commit -m "dotfiles: resolve merge conflict"`
5. `chezmoi apply`

### 快捷命令参考

```bash
# 一键查看 Zed 配置差异
chezmoi diff ~/AppData/Roaming/Zed/

# 只应用 Zed 配置（不碰其他 dotfiles）
chezmoi apply ~/AppData/Roaming/Zed/settings.json ~/AppData/Roaming/Zed/keymap.json

# 在 chezmoi 源仓库里直接编辑 settings.json
chezmoi edit ~/AppData/Roaming/Zed/settings.json
```
