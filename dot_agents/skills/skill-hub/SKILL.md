---
name: skill-hub
description: "管理个人 skill、Zed 配置及其他 dotfiles 的同步与分发。将 user scope 资产用 chezmoi 纳入版本控制，实现跨电脑一键同步。当用户说 skill hub、同步 skills、skills 管理、skills push/pull、skill 备份、新电脑装 skills、同步 zed 配置、zed chezmoi 时触发。"
---

# Skill Hub

管理个人 skill、Zed 编辑器配置及其他 dotfiles 的同步与分发。

## 触发场景

- "skill hub"
- "同步 skills"
- "skills 管理"
- "skills push / pull"
- "skill 备份"
- "新电脑装 skills"
- "同步 zed 配置"
- "push zed 设置"
- "pull zed 配置"
- "上传/下载 zed 配置"
- "备份 zed 设置"
- "zed chezmoi"

## 架构

| 资产类型 | 本地路径 | chezmoi 源路径 | 说明 |
|----------|----------|----------------|------|
| User scope skills | `~/.agents/skills/` | `dot_agents/skills/` | 通用 skills，跨所有项目可用 |
| Zed 配置 | `~/AppData/Roaming/Zed/` | `AppData/Roaming/Zed/` | Zed 编辑器配置 |
| clang-format | `~/.clang-format` | `dot_clang-format` | C++ 全局格式化配置 |

**Project scope skills**（`<vault>/.agents/skills/`）跟随 vault git 同步，不由 chezmoi 管理。

## 环境信息

- chezmoi 本地仓库：`~/.local/share/chezmoi/`
- 远程仓库：`https://github.com/asxiuxiu/dotfiles.git`
- User scope skills 源目录：`dot_agents/skills/`（chezmoi 内部路径名）
- Zed 配置目录（Windows）：`~/AppData/Roaming/Zed/`

## 子命令

### skills push（推送 skills 变更到远程）

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

### skills pull（拉取远程 skills 并应用）

```bash
cd ~/.local/share/chezmoi
chezmoi git -- pull
chezmoi apply ~/.agents/skills/
```

应用前可先执行 `chezmoi diff ~/.agents/skills/` 确认变更。

### zed push（推送 Zed 配置到远程）

```bash
cd ~/.local/share/chezmoi
chezmoi add ~/AppData/Roaming/Zed/settings.json
chezmoi add ~/AppData/Roaming/Zed/keymap.json
# 如有 themes/、tasks.json、snippets/，一并 chezmoi add
chezmoi git -- diff --stat
chezmoi git -- add -A
chezmoi git -- commit -m "zed: sync config"
chezmoi git -- push
```

### zed pull（拉取远程 Zed 配置并应用）

```bash
cd ~/.local/share/chezmoi
chezmoi git -- pull
chezmoi apply ~/AppData/Roaming/Zed/settings.json ~/AppData/Roaming/Zed/keymap.json
# 如有其他管理的文件，一并 chezmoi apply
```

> 应用前可先执行 `chezmoi diff` 确认变更内容。

### zed add（将新文件加入 Zed 配置管理）

当用户新增了 Zed 自定义主题、任务或代码片段时：

```bash
chezmoi add ~/AppData/Roaming/Zed/themes/my-theme.json
# 或扫描并自动添加所有未管理的相关文件
```

### status（查看所有资产同步状态）

```bash
chezmoi status
chezmoi git -- log --oneline -5
```

查看 Zed 配置具体差异：
```bash
chezmoi diff ~/AppData/Roaming/Zed/
```

查看 skills 具体差异：
```bash
chezmoi diff ~/.agents/skills/
```

### list（列出所有 skills）

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
2. 写入 `SKILL.md` 模板
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

## 环境信息

- 相关路径：...
- 依赖工具：...
```

## 新电脑初始化流程

在一台全新电脑上恢复所有个人资产：

```bash
# 1. 安装 chezmoi
winget install twpayne.chezmoi

# 2. 初始化并拉取 dotfiles
chezmoi init --apply https://github.com/asxiuxiu/dotfiles.git

# 3. 验证已恢复
ls ~/.agents/skills/
ls ~/AppData/Roaming/Zed/
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
4. `chezmoi git -- commit -m "resolve merge conflict"`
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
