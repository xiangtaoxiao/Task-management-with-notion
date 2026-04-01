# Notion 待办事项管理系统 for OpenClaw

## 项目简介

这是一个基于 OpenClaw Skills + Tools 的 Notion 待办事项管理系统插件，支持：

- 用户配置 Notion API Key，实现远程控制
- 自动检查并创建 Notion 数据库（若不存在）
- 基于用户对话，实现任务的增删改查（CRUD）
- 支持任务查询与简报生成
- 支持定时任务，自动提醒即将到期事项

## 技术架构

### Tools 层（底层能力）

- `notion_api_tool` - 封装 Notion API
- `scheduler_tool` - 支持 cron-like 调度
- `storage_tool` - 存储用户配置和数据库ID
- `notification_tool` - 支持发送提醒

### Skills 层（核心逻辑）

#### 基础层
- `notion_init` - 初始化 Notion 连接
- `task_crud` - 任务的增删改查
- `task_query` - 任务查询

#### 业务层
- `task_manager` - 核心入口，协调其他技能
- `task_briefing` - 任务简报生成

#### 自动化层
- `task_monitor` - 定时监控和提醒
- `priority_engine` - 任务优先级计算

## 目录结构

```
notion-plugin/
├── tools/
│   ├── notion_api_tool.py
│   ├── scheduler_tool.py
│   ├── storage_tool.py
│   └── notification_tool.py
├── skills/
│   ├── notion_init/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   ├── task_crud/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   ├── task_query/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   ├── task_manager/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   ├── task_briefing/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   ├── task_monitor/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   └── priority_engine/
│       ├── SKILL.md
│       ├── scripts/
│       └── references/
├── storage/
├── scheduler/
├── config.yaml
└── README.md
```

## 安装步骤

1. **克隆项目**

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置 Notion API**
   - 在 Notion 中创建一个集成（Integration）
   - 获取 API Key
   - 分享需要管理的页面给该集成

4. **配置插件**
   - 复制 `config.yaml` 文件
   - 填入 Notion API Key

5. **初始化插件**
   - 运行初始化脚本，配置 API Key 并创建数据库

## 使用方法

### 初始化 Notion 连接
```bash
python skills/notion_init/scripts/init.py <your_notion_api_key>
```

### 创建任务
```bash
python skills/task_manager/scripts/manager.py create "任务标题"
```

### 查询任务
```bash
python skills/task_manager/scripts/manager.py query today
```

### 生成任务简报
```bash
python skills/task_briefing/scripts/briefing.py
```

### 启动任务监控
```bash
python skills/task_monitor/scripts/monitor.py start
```

## 配置文件说明

`config.yaml` 文件包含以下配置：

- `notion` - Notion API 相关配置
- `scheduler` - 定时任务配置
- `storage` - 存储配置
- `notification` - 通知配置

## 示例用户交互流程

1. **用户**："帮我初始化 Notion 连接"
   **系统**："请提供您的 Notion API Key"
   **用户**："secret_xxxxxxxxxxxxxxxx"
   **系统**："初始化成功！已创建/找到 'To Do List 任务看板' 数据库"

2. **用户**："创建一个任务，标题为 '完成项目报告'，截止日期为明天"
   **系统**："任务创建成功！"

3. **用户**："查看今天的任务"
   **系统**："今天有 2 个任务：1. 完成项目报告 2. 参加团队会议"

4. **用户**："生成任务简报"
   **系统**："任务简报已生成，总任务数：10，今日任务：2，即将到期：3，已完成：5"

## 安全要求

- 不执行用户原始命令
- 不暴露 API key
- 限制 tool 权限
- 所有外部调用必须经过 tool 封装

## 注意事项

- 首次使用需要初始化 Notion 连接
- 需要确保 Notion 集成有足够的权限
- 定时任务需要保持进程运行
- 建议定期备份 Notion 数据
