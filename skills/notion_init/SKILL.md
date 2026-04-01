---
name: notion_init
description: 初始化Notion连接，配置API密钥并创建数据库
---

## When to use
- 首次使用Notion插件时
- 需要更新Notion API密钥时
- Notion数据库不存在需要创建时

## Instructions
1. 接收用户提供的Notion API密钥
2. 验证API密钥的有效性
3. 搜索现有的"To Do List 任务看板"数据库
4. 如果数据库不存在，创建一个新的数据库
5. 存储数据库ID和用户配置
6. 返回初始化结果

## Tools
- notion_api_tool: 用于搜索和创建数据库
- storage_tool: 用于存储用户配置和数据库ID

## Output format
```json
{
  "status": "success" or "error",
  "message": "初始化结果消息",
  "database_id": "数据库ID",
  "database_name": "To Do List 任务看板"
}
```
