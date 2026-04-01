---
name: task_crud
description: 任务的增删改查操作
---

## When to use
- 需要创建新任务时
- 需要更新现有任务时
- 需要删除任务时
- 需要获取任务详情时

## Instructions
1. 接收用户请求和任务数据
2. 加载存储的Notion API密钥和数据库ID
3. 初始化Notion API工具
4. 根据操作类型执行相应的CRUD操作
5. 返回操作结果

## Tools
- notion_api_tool: 用于执行任务的增删改查操作
- storage_tool: 用于加载用户配置和数据库ID

## Output format
```json
{
  "status": "success" or "error",
  "message": "操作结果消息",
  "task": {
    "id": "任务ID",
    "title": "任务标题",
    "status": "任务状态",
    "due_date": "截止日期",
    "priority": "优先级"
  }
}
```
