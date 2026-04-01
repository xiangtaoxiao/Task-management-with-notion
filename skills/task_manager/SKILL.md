---
name: task_manager
description: 任务管理系统核心入口，协调其他技能
---

## When to use
- 作为任务管理系统的主入口
- 需要处理复杂的任务管理请求时
- 需要协调多个子技能完成任务时

## Instructions
1. 接收用户的任务管理请求
2. 分析请求类型并调用相应的子技能
3. 整合子技能的执行结果
4. 返回统一的处理结果

## Tools
- notion_init: 用于初始化Notion连接
- task_crud: 用于任务的增删改查
- task_query: 用于任务查询
- storage_tool: 用于存储和加载配置

## Output format
```json
{
  "status": "success" or "error",
  "message": "处理结果消息",
  "data": {
    "type": "init|create|update|delete|query",
    "result": "具体处理结果"
  }
}
```
