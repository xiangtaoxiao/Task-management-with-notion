---
name: task_query
description: 任务查询和筛选
---

## When to use
- 需要查询今天的任务时
- 需要查询即将到期的任务时
- 需要查询已完成的任务时
- 需要根据其他条件查询任务时

## Instructions
1. 接收用户的查询请求和筛选条件
2. 加载存储的Notion API密钥和数据库ID
3. 初始化Notion API工具
4. 根据筛选条件构建查询
5. 执行查询并获取结果
6. 返回查询结果

## Tools
- notion_api_tool: 用于执行数据库查询
- storage_tool: 用于加载用户配置和数据库ID

## Output format
```json
{
  "status": "success" or "error",
  "message": "查询结果消息",
  "tasks": [
    {
      "id": "任务ID",
      "title": "任务标题",
      "status": "任务状态",
      "due_date": "截止日期",
      "priority": "优先级"
    }
  ],
  "total": "任务总数"
}
```
