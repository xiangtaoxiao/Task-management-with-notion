---
name: task_briefing
description: 任务简报生成
---

## When to use
- 需要生成任务简报时
- 需要了解任务概览时
- 需要定期汇报任务状态时

## Instructions
1. 加载存储的Notion API密钥和数据库ID
2. 初始化Notion API工具
3. 查询不同状态的任务
4. 生成任务简报
5. 返回简报结果

## Tools
- task_query: 用于查询任务
- storage_tool: 用于加载用户配置和数据库ID

## Output format
```json
{
  "status": "success" or "error",
  "message": "简报生成结果消息",
  "briefing": {
    "total_tasks": "总任务数",
    "today_tasks": "今日任务数",
    "upcoming_tasks": "即将到期任务数",
    "completed_tasks": "已完成任务数",
    "tasks_by_status": {
      "待办": "数量",
      "进行中": "数量",
      "已完成": "数量",
      "已取消": "数量"
    },
    "tasks_by_priority": {
      "重要紧急": "数量",
      "重要不紧急": "数量",
      "紧急不重要": "数量",
      "不重要不紧急": "数量"
    }
  }
}
```
