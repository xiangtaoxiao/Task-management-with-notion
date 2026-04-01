import json
from skills.notion_init.scripts.init import NotionInitSkill
from skills.task_crud.scripts.crud import TaskCRUDSkill
from skills.task_query.scripts.query import TaskQuerySkill
from tools.storage_tool import StorageTool

class TaskManagerSkill:
    def __init__(self):
        self.init_skill = NotionInitSkill()
        self.crud_skill = TaskCRUDSkill()
        self.query_skill = TaskQuerySkill()
        self.storage = StorageTool()
    
    def handle_request(self, request_type, **kwargs):
        """Handle task management requests"""
        try:
            if request_type == "init":
                # Initialize Notion connection
                api_key = kwargs.get("api_key")
                if not api_key:
                    return {
                        "status": "error",
                        "message": "API key is required",
                        "data": {
                            "type": "init",
                            "result": None
                        }
                    }
                
                result = self.init_skill.run(api_key)
                return {
                    "status": result["status"],
                    "message": result["message"],
                    "data": {
                        "type": "init",
                        "result": result
                    }
                }
            
            elif request_type == "create":
                # Create task
                title = kwargs.get("title")
                if not title:
                    return {
                        "status": "error",
                        "message": "Task title is required",
                        "data": {
                            "type": "create",
                            "result": None
                        }
                    }
                
                description = kwargs.get("description", "")
                category = kwargs.get("category", "")
                status = kwargs.get("status", "待办")
                priority = kwargs.get("priority", "")
                due_date = kwargs.get("due_date")
                
                result = self.crud_skill.create_task(
                    title, description, category, status, priority, due_date
                )
                return {
                    "status": result["status"],
                    "message": result["message"],
                    "data": {
                        "type": "create",
                        "result": result
                    }
                }
            
            elif request_type == "update":
                # Update task
                task_id = kwargs.get("task_id")
                if not task_id:
                    return {
                        "status": "error",
                        "message": "Task ID is required",
                        "data": {
                            "type": "update",
                            "result": None
                        }
                    }
                
                title = kwargs.get("title")
                description = kwargs.get("description")
                category = kwargs.get("category")
                status = kwargs.get("status")
                priority = kwargs.get("priority")
                due_date = kwargs.get("due_date")
                
                result = self.crud_skill.update_task(
                    task_id, title, description, category, status, priority, due_date
                )
                return {
                    "status": result["status"],
                    "message": result["message"],
                    "data": {
                        "type": "update",
                        "result": result
                    }
                }
            
            elif request_type == "delete":
                # Delete task
                task_id = kwargs.get("task_id")
                if not task_id:
                    return {
                        "status": "error",
                        "message": "Task ID is required",
                        "data": {
                            "type": "delete",
                            "result": None
                        }
                    }
                
                result = self.crud_skill.delete_task(task_id)
                return {
                    "status": result["status"],
                    "message": result["message"],
                    "data": {
                        "type": "delete",
                        "result": result
                    }
                }
            
            elif request_type == "get":
                # Get task
                task_id = kwargs.get("task_id")
                if not task_id:
                    return {
                        "status": "error",
                        "message": "Task ID is required",
                        "data": {
                            "type": "get",
                            "result": None
                        }
                    }
                
                result = self.crud_skill.get_task(task_id)
                return {
                    "status": result["status"],
                    "message": result["message"],
                    "data": {
                        "type": "get",
                        "result": result
                    }
                }
            
            elif request_type == "query":
                # Query tasks
                query_type = kwargs.get("query_type", "today")
                
                if query_type == "today":
                    result = self.query_skill.query_today_tasks()
                elif query_type == "upcoming":
                    result = self.query_skill.query_upcoming_tasks()
                elif query_type == "completed":
                    result = self.query_skill.query_completed_tasks()
                elif query_type == "status":
                    status = kwargs.get("status")
                    if not status:
                        return {
                            "status": "error",
                            "message": "Status is required for status query",
                            "data": {
                                "type": "query",
                                "result": None
                            }
                        }
                    result = self.query_skill.query_tasks_by_status(status)
                else:
                    return {
                        "status": "error",
                        "message": f"Invalid query type: {query_type}",
                        "data": {
                            "type": "query",
                            "result": None
                        }
                    }
                
                return {
                    "status": result["status"],
                    "message": result["message"],
                    "data": {
                        "type": "query",
                        "result": result
                    }
                }
            
            else:
                return {
                    "status": "error",
                    "message": f"Invalid request type: {request_type}",
                    "data": {
                        "type": "error",
                        "result": None
                    }
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to handle request: {str(e)}",
                "data": {
                    "type": request_type,
                    "result": None
                }
            }

if __name__ == "__main__":
    # For testing
    import sys
    manager = TaskManagerSkill()
    
    if len(sys.argv) > 2:
        request_type = sys.argv[1]
        
        if request_type == "init" and len(sys.argv) > 2:
            api_key = sys.argv[2]
            result = manager.handle_request("init", api_key=api_key)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif request_type == "create" and len(sys.argv) > 2:
            title = sys.argv[2]
            result = manager.handle_request("create", title=title)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif request_type == "query" and len(sys.argv) > 2:
            query_type = sys.argv[2]
            result = manager.handle_request("query", query_type=query_type)
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Usage: python manager.py [init|create|update|delete|get|query] [parameters]")
