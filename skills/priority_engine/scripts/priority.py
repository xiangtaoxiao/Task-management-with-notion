import json
from datetime import datetime, timedelta
from tools.notion_api_tool import NotionAPITool
from tools.storage_tool import StorageTool

class PriorityEngineSkill:
    def __init__(self):
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
    
    def calculate_priority(self):
        """Calculate and update task priorities"""
        try:
            notion = self._get_notion_client()
            database_id = self._get_database_id()
            
            # Get all tasks
            all_tasks = notion.query_database(database_id)
            
            updated_tasks = []
            
            for task in all_tasks:
                # Get task properties
                task_id = task["id"]
                title = self._get_page_title(task)
                due_date = self._get_page_property(task, "截止日期")
                status = self._get_page_property(task, "状态")
                old_priority = self._get_page_property(task, "四象限")
                
                # Skip completed or cancelled tasks
                if status in ["已完成", "已取消"]:
                    continue
                
                # Calculate new priority based on due date
                new_priority = old_priority
                
                if due_date:
                    due_date_obj = datetime.fromisoformat(due_date)
                    now = datetime.now()
                    time_until_due = due_date_obj - now
                    
                    # Calculate priority based on time until due
                    if time_until_due < timedelta(hours=24):
                        # Urgent
                        if time_until_due < timedelta(hours=2):
                            new_priority = "重要紧急"
                        else:
                            new_priority = "紧急不重要"
                    else:
                        # Not urgent
                        # For now, keep existing priority or set to important not urgent
                        if not old_priority:
                            new_priority = "重要不紧急"
                else:
                    # No due date, set to not important not urgent
                    if not old_priority:
                        new_priority = "不重要不紧急"
                
                # Update priority if changed
                if new_priority != old_priority:
                    # Update task
                    properties = {
                        "四象限": {
                            "select": {
                                "name": new_priority
                            }
                        }
                    }
                    notion.update_page(task_id, properties)
                    
                    # Add to updated tasks
                    updated_tasks.append({
                        "task_id": task_id,
                        "title": title,
                        "old_priority": old_priority or "",
                        "new_priority": new_priority
                    })
            
            return {
                "status": "success",
                "message": f"Calculated priorities for {len(all_tasks)} tasks, updated {len(updated_tasks)} tasks",
                "updated_tasks": updated_tasks,
                "total_updated": len(updated_tasks)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to calculate priorities: {str(e)}",
                "updated_tasks": [],
                "total_updated": 0
            }
    
    def _get_page_title(self, page):
        """Get page title from page object"""
        if "properties" in page and "待办事项" in page["properties"]:
            title_prop = page["properties"]["待办事项"]
            if title_prop["type"] == "title" and title_prop["title"]:
                return "".join([text["plain_text"] for text in title_prop["title"]])
        return ""
    
    def _get_page_property(self, page, property_name):
        """Get property value from page object"""
        if "properties" in page and property_name in page["properties"]:
            prop = page["properties"][property_name]
            prop_type = prop["type"]
            
            if prop_type == "select" and prop["select"]:
                return prop["select"]["name"]
            elif prop_type == "status" and prop["status"]:
                return prop["status"]["name"]
            elif prop_type == "date" and prop["date"]:
                return prop["date"]["start"]
        return ""

if __name__ == "__main__":
    # For testing
    skill = PriorityEngineSkill()
    result = skill.calculate_priority()
    print(json.dumps(result, indent=2, ensure_ascii=False))
