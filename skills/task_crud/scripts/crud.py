import json
from tools.notion_api_tool import NotionAPITool
from tools.storage_tool import StorageTool

class TaskCRUDSkill:
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
    
    def create_task(self, title, description="", category="", status="待办", priority="", due_date=None):
        """Create a new task"""
        try:
            notion = self._get_notion_client()
            database_id = self._get_database_id()
            
            # Prepare properties
            properties = {
                "待办事项": {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": title
                            }
                        }
                    ]
                }
            }
            
            # Add optional properties
            if description:
                properties["备注"] = {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": description
                            }
                        }
                    ]
                }
            
            if category:
                properties["类别"] = {
                    "select": {
                        "name": category
                    }
                }
            
            if status:
                properties["状态"] = {
                    "status": {
                        "name": status
                    }
                }
            
            if priority:
                properties["四象限"] = {
                    "select": {
                        "name": priority
                    }
                }
            
            if due_date:
                properties["截止日期"] = {
                    "date": {
                        "start": due_date
                    }
                }
            
            # Create page
            page = notion.create_page(database_id, properties)
            
            return {
                "status": "success",
                "message": "Task created successfully",
                "task": {
                    "id": page["id"],
                    "title": title,
                    "status": status,
                    "due_date": due_date,
                    "priority": priority
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create task: {str(e)}",
                "task": None
            }
    
    def update_task(self, task_id, title=None, description=None, category=None, status=None, priority=None, due_date=None):
        """Update an existing task"""
        try:
            notion = self._get_notion_client()
            
            # Prepare properties
            properties = {}
            
            if title:
                properties["待办事项"] = {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": title
                            }
                        }
                    ]
                }
            
            if description is not None:
                properties["备注"] = {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": description
                            }
                        }
                    ]
                }
            
            if category:
                properties["类别"] = {
                    "select": {
                        "name": category
                    }
                }
            
            if status:
                properties["状态"] = {
                    "status": {
                        "name": status
                    }
                }
            
            if priority:
                properties["四象限"] = {
                    "select": {
                        "name": priority
                    }
                }
            
            if due_date:
                properties["截止日期"] = {
                    "date": {
                        "start": due_date
                    }
                }
            
            # Update page
            page = notion.update_page(task_id, properties)
            
            # Get updated task details
            updated_page = notion.get_page(task_id)
            
            return {
                "status": "success",
                "message": "Task updated successfully",
                "task": {
                    "id": page["id"],
                    "title": title or self._get_page_title(updated_page),
                    "status": status or self._get_page_property(updated_page, "状态"),
                    "due_date": due_date or self._get_page_property(updated_page, "截止日期"),
                    "priority": priority or self._get_page_property(updated_page, "四象限")
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to update task: {str(e)}",
                "task": None
            }
    
    def delete_task(self, task_id):
        """Delete a task"""
        try:
            notion = self._get_notion_client()
            
            # Delete page
            notion.delete_page(task_id)
            
            return {
                "status": "success",
                "message": "Task deleted successfully",
                "task": {
                    "id": task_id
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete task: {str(e)}",
                "task": None
            }
    
    def get_task(self, task_id):
        """Get task details"""
        try:
            notion = self._get_notion_client()
            
            # Get page
            page = notion.get_page(task_id)
            
            return {
                "status": "success",
                "message": "Task retrieved successfully",
                "task": {
                    "id": page["id"],
                    "title": self._get_page_title(page),
                    "status": self._get_page_property(page, "状态"),
                    "due_date": self._get_page_property(page, "截止日期"),
                    "priority": self._get_page_property(page, "四象限")
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get task: {str(e)}",
                "task": None
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
    skill = TaskCRUDSkill()
    
    if len(sys.argv) > 2:
        action = sys.argv[1]
        
        if action == "create":
            title = sys.argv[2]
            result = skill.create_task(title)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif action == "update":
            task_id = sys.argv[2]
            title = sys.argv[3] if len(sys.argv) > 3 else None
            result = skill.update_task(task_id, title=title)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif action == "delete":
            task_id = sys.argv[2]
            result = skill.delete_task(task_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif action == "get":
            task_id = sys.argv[2]
            result = skill.get_task(task_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Usage: python crud.py [create|update|delete|get] [task_id/title] [optional parameters]")
