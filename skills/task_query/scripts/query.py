import json
from datetime import datetime, timedelta
from tools.notion_api_tool import NotionAPITool
from tools.storage_tool import StorageTool

class TaskQuerySkill:
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
    
    def query_today_tasks(self):
        """Query tasks due today"""
        try:
            notion = self._get_notion_client()
            database_id = self._get_database_id()
            
            # Get today's date in ISO format
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Build filter
            filter = {
                "and": [
                    {
                        "property": "截止日期",
                        "date": {
                            "equals": today
                        }
                    },
                    {
                        "property": "状态",
                        "status": {
                            "does_not_equal": "已完成"
                        }
                    }
                ]
            }
            
            # Execute query
            results = notion.query_database(database_id, filter)
            
            # Format results
            tasks = []
            for page in results:
                tasks.append({
                    "id": page["id"],
                    "title": self._get_page_title(page),
                    "status": self._get_page_property(page, "状态"),
                    "due_date": self._get_page_property(page, "截止日期"),
                    "priority": self._get_page_property(page, "四象限")
                })
            
            return {
                "status": "success",
                "message": f"Found {len(tasks)} tasks due today",
                "tasks": tasks,
                "total": len(tasks)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to query tasks: {str(e)}",
                "tasks": [],
                "total": 0
            }
    
    def query_upcoming_tasks(self):
        """Query tasks due in the next 7 days"""
        try:
            notion = self._get_notion_client()
            database_id = self._get_database_id()
            
            # Get date range
            today = datetime.now().strftime("%Y-%m-%d")
            next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            
            # Build filter
            filter = {
                "and": [
                    {
                        "property": "截止日期",
                        "date": {
                            "on_or_after": today,
                            "on_or_before": next_week
                        }
                    },
                    {
                        "property": "状态",
                        "status": {
                            "does_not_equal": "已完成"
                        }
                    }
                ]
            }
            
            # Execute query
            results = notion.query_database(database_id, filter)
            
            # Format results
            tasks = []
            for page in results:
                tasks.append({
                    "id": page["id"],
                    "title": self._get_page_title(page),
                    "status": self._get_page_property(page, "状态"),
                    "due_date": self._get_page_property(page, "截止日期"),
                    "priority": self._get_page_property(page, "四象限")
                })
            
            return {
                "status": "success",
                "message": f"Found {len(tasks)} upcoming tasks",
                "tasks": tasks,
                "total": len(tasks)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to query tasks: {str(e)}",
                "tasks": [],
                "total": 0
            }
    
    def query_completed_tasks(self):
        """Query completed tasks"""
        try:
            notion = self._get_notion_client()
            database_id = self._get_database_id()
            
            # Build filter
            filter = {
                "property": "状态",
                "status": {
                    "equals": "已完成"
                }
            }
            
            # Execute query
            results = notion.query_database(database_id, filter)
            
            # Format results
            tasks = []
            for page in results:
                tasks.append({
                    "id": page["id"],
                    "title": self._get_page_title(page),
                    "status": self._get_page_property(page, "状态"),
                    "due_date": self._get_page_property(page, "截止日期"),
                    "priority": self._get_page_property(page, "四象限")
                })
            
            return {
                "status": "success",
                "message": f"Found {len(tasks)} completed tasks",
                "tasks": tasks,
                "total": len(tasks)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to query tasks: {str(e)}",
                "tasks": [],
                "total": 0
            }
    
    def query_tasks_by_status(self, status):
        """Query tasks by status"""
        try:
            notion = self._get_notion_client()
            database_id = self._get_database_id()
            
            # Build filter
            filter = {
                "property": "状态",
                "status": {
                    "equals": status
                }
            }
            
            # Execute query
            results = notion.query_database(database_id, filter)
            
            # Format results
            tasks = []
            for page in results:
                tasks.append({
                    "id": page["id"],
                    "title": self._get_page_title(page),
                    "status": self._get_page_property(page, "状态"),
                    "due_date": self._get_page_property(page, "截止日期"),
                    "priority": self._get_page_property(page, "四象限")
                })
            
            return {
                "status": "success",
                "message": f"Found {len(tasks)} tasks with status '{status}'",
                "tasks": tasks,
                "total": len(tasks)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to query tasks: {str(e)}",
                "tasks": [],
                "total": 0
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
    import sys
    skill = TaskQuerySkill()
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "today":
            result = skill.query_today_tasks()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif action == "upcoming":
            result = skill.query_upcoming_tasks()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif action == "completed":
            result = skill.query_completed_tasks()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif action == "status" and len(sys.argv) > 2:
            status = sys.argv[2]
            result = skill.query_tasks_by_status(status)
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Usage: python query.py [today|upcoming|completed|status] [status_value]")
