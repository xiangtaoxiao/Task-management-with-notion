---
name: task_monitor
description: 任务监控和提醒
---

## When to use
- 需要定时监控任务状态时
- 需要自动提醒即将到期的任务时
- 需要监控任务进展时

## Instructions
1. 加载存储的Notion API密钥和数据库ID
2. 初始化Notion API工具
3. 查询即将到期的任务
4. 根据任务截止时间计算优先级
5. 发送相应的提醒通知
6. 返回监控结果

## Tools
- task_query: 用于查询任务
- notification_tool: 用于发送提醒
- scheduler_tool: 用于定时执行监控
- storage_tool: 用于加载用户配置和数据库ID

## Output format
```json
{
  "status": "success" or "error",
  "message": "监控结果消息",
  "alerts": [
    {
      "task_id": "任务ID",
      "title": "任务标题",
      "due_date": "截止日期",
      "priority": "优先级",
      "alert_level": "urgent|high|normal"
    }
  ],
  "total_alerts": "提醒总数"
}
```
