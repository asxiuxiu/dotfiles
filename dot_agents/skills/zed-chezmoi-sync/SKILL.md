---
name: zed-chezmoi-sync
description: 用 chezmoi 将 Zed 编辑器配置同步到远程 dotfiles 仓库。当用户说"同步 zed 配置"、"push zed 设置"、"pull zed 配置"、"备份 zed 设置"或"zed chezmoi"时触发。
---

# Zed Chezmoi 同步 Skill

用 chezmoi 将 Zed 编辑器配置同步到远程 dotfiles 仓库（`https://github.com/asxiuxiu/dotfiles.git`）。

## 触发场景

当用户说以下任意内容时触发：
- "同步 zed 配置"
- "push zed 设置"
- "pull zed 配置"
- "上传/下载 zed 配置"
- "备份 zed 设置"
- "zed chezmoi"

## 环境信息

| 项目 | 路径/值 |
|------|---------|
| chezmoi 本地仓库 | `~/.local/share/chezmoi/` |
| 远程仓库 | `https://github.com/asxiuxiu/dotfiles.git` |
| Zed 配置目录（Windows） | `~/AppData/Roaming/Zed/`（即 `$APPDATA/Zed/`） |
| chezmoi 源文件路径 | `AppData/Roaming/Zed/` |

## 需要同步的文件

| 文件/目录 | 说明 |
|-----------|------|
| `settings.json` | Zed 核心设置 |
| `keymap.json` | 键位映射 |
| `themes/` | 自定义主题（如有） |
| `tasks.json` | 用户自定义任务（如有） |
| `snippets/` | 代码片段（如有） |

**不同步的运行时目录**（由 chezmoi 的 `.chezmoiignore` 或手动排除）：
`db/`, `extensions/`, `languages/`, `logs/`, `node/`, `prompts/`, `threads/`, `debug_adapters/`, `prettier/`, `hang_traces/`, `external_agents/`, `zed-crash-handler-*`

## 子命令

### push（推送当前配置到远程）

将本地 Zed 配置的变更提交并推送到远程仓库。

步骤：
1. `cd ~/.local/share/chezmoi`
2. `chezmoi add ~/AppData/Roaming/Zed/settings.json`
3. `chezmoi add ~/AppData/Roaming/Zed/keymap.json`
4. 如有 `themes/`、`tasks.json`、`snippets/`，一并 `chezmoi add`
5. `chezmoi git -- diff --stat` 或 `git diff --cached --stat` 查看变更摘要
6. `chezmoi git -- add -A`
7. `chezmoi git -- commit -m "zed: sync config"`（若用户提供了消息，使用用户消息）
8. `chezmoi git -- push`

### pull（拉取远程配置并应用）

从远程仓库拉取最新 Zed 配置并应用到本地。

步骤：
1. `cd ~/.local/share/chezmoi`
2. `chezmoi git -- pull`
3. `chezmoi apply ~/AppData/Roaming/Zed/settings.json ~/AppData/Roaming/Zed/keymap.json`
4. 如有其他管理的文件，一并 `chezmoi apply`

> **注意**：应用前可先执行 `chezmoi diff` 确认变更内容，避免覆盖本地未备份的修改。

### status（查看同步状态）

查看本地 Zed 配置与 chezmoi 仓库的差异。

步骤：
1. `cd ~/.local/share/chezmoi`
2. `chezmoi status` — 查看 chezmoi 管理的文件状态
3. `chezmoi diff ~/AppData/Roaming/Zed/` — 查看 Zed 配置的具体差异
4. `chezmoi git -- log --oneline -5` — 查看最近的提交历史

### add（将新文件加入管理）

当用户新增了 Zed 自定义主题、任务或代码片段时，将其加入 chezmoi 管理。

用法示例：将 `themes/my-theme.json` 加入管理：
1. `chezmoi add ~/AppData/Roaming/Zed/themes/my-theme.json`

或者扫描并自动添加所有未管理的相关文件：
1. 遍历 `~/AppData/Roaming/Zed/` 下 `settings.json`、`keymap.json`、`tasks.json`、`snippets/`、`themes/`
2. 对每个文件执行 `chezmoi add`（chezmoi 对已管理文件是幂等的）

## 常见问题

### Zed 配置路径确认
Windows 上 Zed 使用 `AppData/Roaming/Zed/` 存放配置。如果未来 Zed 更改了配置目录位置，需同步更新本 skill 中的路径。

### 避免覆盖本地修改
执行 `pull`/`apply` 前，先运行 `chezmoi diff` 查看差异，确认没有本地未提交的修改会被覆盖。

### 合并冲突
如果本地和远程同时修改了同一文件，`chezmoi git -- pull` 会产生冲突。此时需要：
1. 进入 `~/.local/share/chezmoi` 目录
2. 手动解决 `AppData/Roaming/Zed/` 下的冲突文件
3. `chezmoi git -- add -A`
4. `chezmoi git -- commit -m "zed: resolve merge conflict"`
5. `chezmoi apply`

## 快捷命令参考

```bash
# 一键查看 Zed 配置差异
chezmoi diff ~/AppData/Roaming/Zed/

# 只应用 Zed 配置（不碰其他 dotfiles）
chezmoi apply ~/AppData/Roaming/Zed/settings.json ~/AppData/Roaming/Zed/keymap.json

# 在 chezmoi 源仓库里直接编辑 settings.json
chezmoi edit ~/AppData/Roaming/Zed/settings.json
```
