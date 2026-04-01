---
name: priority_engine
description: 任务优先级计算引擎
---

## When to use
- 需要自动计算任务优先级时
- 需要根据任务属性调整优先级时
- 需要优化任务排序时

## Instructions
1. 加载存储的Notion API密钥和数据库ID
2. 初始化Notion API工具
3. 查询所有任务
4. 根据任务属性计算优先级
5. 更新任务优先级
6. 返回优先级计算结果

## Tools
- notion_api_tool: 用于获取和更新任务
- storage_tool: 用于加载用户配置和数据库ID

## Output format
```json
{
  "status": "success" or "error",
  "message": "优先级计算结果消息",
  "updated_tasks": [
    {
      "task_id": "任务ID",
      "title": "任务标题",
      "old_priority": "旧优先级",
      "new_priority": "新优先级"
    }
  ],
  "total_updated": "更新任务总数"
}
```
