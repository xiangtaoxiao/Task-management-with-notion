import json
from skills.task_query.scripts.query import TaskQuerySkill
from tools.notion_api_tool import NotionAPITool
from tools.storage_tool import StorageTool

class TaskBriefingSkill:
    def __init__(self):
        self.query_skill = TaskQuerySkill()
        self.storage = StorageTool()
    
    def _get_notion_client(self):
        """Get Notion client from stored config"""
        config = self.storage.get_user_config()
        api_key = config.get("api_key")
        if not api_key:
            raise ValueError("Notion API key not configured")
        return NotionAPITool(api_key)
    
    def _get_database_id(self):
        """Get database ID from storage"""
        database_id = self.storage.get_database_id()
        if not database_id:
            raise ValueError("Database ID not configured")
        return database_id
    
    def generate_briefing(self):
        """Generate task briefing"""
        try:
            # Get tasks by different categories
            today_tasks = self.query_skill.query_today_tasks()
            upcoming_tasks = self.query_skill.query_upcoming_tasks()
            completed_tasks = self.query_skill.query_completed_tasks()
            
            # Get tasks by status
            todo_tasks = self.query_skill.query_tasks_by_status("待办")
            in_progress_tasks = self.query_skill.query_tasks_by_status("进行中")
            completed_tasks_status = self.query_skill.query_tasks_by_status("已完成")
            cancelled_tasks = self.query_skill.query_tasks_by_status("已取消")
            
            # Get all tasks to count total
            notion = self._get_notion_client()
            database_id = self._get_database_id()
            all_tasks = notion.query_database(database_id)
            
            # Count tasks by priority
            priority_count = {
                "重要紧急": 0,
                "重要不紧急": 0,
                "紧急不重要": 0,
                "不重要不紧急": 0
            }
            
            for task in all_tasks:
                priority = self._get_page_property(task, "四象限")
                if priority in priority_count:
                    priority_count[priority] += 1
            
            # Generate briefing
            briefing = {
                "total_tasks": len(all_tasks),
                "today_tasks": today_tasks["total"],
                "upcoming_tasks": upcoming_tasks["total"],
                "completed_tasks": completed_tasks["total"],
                "tasks_by_status": {
                    "待办": todo_tasks["total"],
                    "进行中": in_progress_tasks["total"],
                    "已完成": completed_tasks_status["total"],
                    "已取消": cancelled_tasks["total"]
                },
                "tasks_by_priority": priority_count
            }
            
            return {
                "status": "success",
                "message": "Task briefing generated successfully",
                "briefing": briefing
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to generate briefing: {str(e)}",
                "briefing": None
            }
    
    def _get_page_property(self, page, property_name):
        """Get property value from page object"""
        if "properties" in page and property_name in page["properties"]:
            prop = page["properties"][property_name]
            prop_type = prop["type"]
            
            if prop_type == "select" and prop["select"]:
                return prop["select"]["name"]
        return ""

if __name__ == "__main__":
    # For testing
    skill = TaskBriefingSkill()
    result = skill.generate_briefing()
    print(json.dumps(result, indent=2, ensure_ascii=False))
