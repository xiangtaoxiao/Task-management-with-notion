# 基于NOTION代办事项与日程管理技能 for OpenClaw

请阅读Openclaw的开发文档以了解tools、skill、plugin的开发规范[https://docs.openclaw.ai/](https://docs.openclaw.ai/tools/creating-skills)

你是一个高级 AI Coding Agent，负责为 OpenClaw 构建一个完整的「Notion 待办事项管理系统」插件。

请严格按照以下要求完成插件设计与代码实现。

# 项目目标

构建一个基于 OpenClaw Skills + Tools 的任务管理系统插件，支持：

1. 用户配置 Notion API Key，实现远程控制
2. 自动检查并创建 Notion 数据库（若不存在）
3. 基于用户对话，实现任务的增删改查（CRUD）
4. 支持任务查询与简报生成
5. 支持定时任务，自动提醒即将到期事项

***

# 技术架构要求

请实现以下模块：

## 1. Tools 层（底层能力）

必须实现：

- notion\_api\_tool
  - 封装 Notion API（禁止直接拼HTTP）
  - 支持：
    - search database
    - create database
    - query database
    - create/update/delete page
- scheduler\_tool
  - 支持 cron-like 调度
  - 至少支持每天：
    - 09:00
    - 14:00
    - 20:00
- storage\_tool
  - 存储：
    - notion\_database\_id
    - user\_config（API key）
- notification\_tool（可选）
  - 支持发送提醒（console / webhook / telegram/Wechat/QQ）

***

## 2. Skills 层（核心逻辑）

请拆分为多个独立 Skill，每个 Skill 遵循 OpenClaw 标准：

每个 Skill 必须包含：

- SKILL.md
- 必要的 scripts/
- references/

必须实现以下 Skills：

### 基础层

- notion\_init
- task\_crud
- task\_query

### 业务层

- task\_manager（核心入口）
- task\_briefing

### 自动化层

- task\_monitor（定时触发）
- priority\_engine

***

# 目录结构要求

请输出完整项目结构：

project-root/\
tools/\
skills/\
notion\_init/\
task\_crud/\
task\_query/\
task\_manager/\
task\_briefing/\
task\_monitor/\
priority\_engine/\
storage/\
scheduler/

***

# Skill设计规范（必须遵守）

请确保所有 SKILL.md：

1. 使用 YAML frontmatter（name + description）
2. 包含：
   - When to use
   - Instructions（step-by-step）
   - Tools
   - Output format
3. 每个 Skill 只做一件事（单一职责）
4. 使用结构化输出（JSON）
5. 不允许模糊语言（必须明确步骤）

***

# Notion数据库设计

必须创建数据库 schema：基于"To Do List 任务看板"

***

# 行为逻辑要求

## 任务创建

从用户输入中解析：

- 标题
- 时间（必须标准化为 ISO）
- 优先级（用户未提及则主动询问，距离当前时间一天以内的默认紧急）

## 查询逻辑

支持：

- 今天任务
- 即将到期
- 已完成

## 提醒逻辑

规则：

- <2小时 → urgent
- <24小时 → high
- 否则 → normal

***

# 安全要求

必须遵守：

- 不执行用户原始命令
- 不暴露 API key
- 限制 tool 权限
- 所有外部调用必须经过 tool 封装

***

# 输出要求（非常重要）

请一次性输出：

1. 完整目录结构
2. 所有 SKILL.md 内容
3. 所有 tool 实现代码（Node.js 或 Python）
4. 示例配置文件（config.yaml）
5. scheduler 实现方案（含代码）
6. 示例用户交互流程

***

# 约束

- 不要省略任何关键文件
- 不要只写示例，必须可运行
- 不要写伪代码，必须是真实代码
- 所有路径必须正确

