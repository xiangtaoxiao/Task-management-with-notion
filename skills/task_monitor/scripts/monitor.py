import json
from datetime import datetime, timedelta
from skills.task_query.scripts.query import TaskQuerySkill
from tools.notion_api_tool import NotionAPITool
from tools.storage_tool import StorageTool
from tools.notification_tool import NotificationTool
from tools.scheduler_tool import SchedulerTool

class TaskMonitorSkill:
    def __init__(self):
        self.query_skill = TaskQuerySkill()
        self.storage = StorageTool()
        self.notification = NotificationTool()
        self.scheduler = SchedulerTool()
    
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
    
    def monitor_tasks(self):
        """Monitor tasks and send alerts"""
        try:
            # Get upcoming tasks
            upcoming_tasks = self.query_skill.query_upcoming_tasks()
            
            alerts = []
            
            # Check each task for alert level
            for task in upcoming_tasks["tasks"]:
                if task["due_date"]:
                    # Calculate time until due date
                    due_date = datetime.fromisoformat(task["due_date"])
                    now = datetime.now()
                    time_until_due = due_date - now
                    
                    # Determine alert level
                    if time_until_due < timedelta(hours=2):
                        alert_level = "urgent"
                    elif time_until_due < timedelta(days=1):
                        alert_level = "high"
                    else:
                        alert_level = "normal"
                    
                    # Add to alerts
                    alerts.append({
                        "task_id": task["id"],
                        "title": task["title"],
                        "due_date": task["due_date"],
                        "priority": task["priority"],
                        "alert_level": alert_level
                    })
            
            # Send notifications for urgent and high priority tasks
            for alert in alerts:
                if alert["alert_level"] in ["urgent", "high"]:
                    message = f"【{alert['alert_level'].upper()}】任务 '{alert['title']}' 即将到期！\n截止日期: {alert['due_date']}\n优先级: {alert['priority']}"
                    self.notification.send_notification(message, "warning" if alert["alert_level"] == "high" else "error")
            
            return {
                "status": "success",
                "message": f"Monitored {len(upcoming_tasks['tasks'])} tasks, found {len(alerts)} alerts",
                "alerts": alerts,
                "total_alerts": len(alerts)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to monitor tasks: {str(e)}",
                "alerts": [],
                "total_alerts": 0
            }
    
    def start_monitoring(self):
        """Start scheduled monitoring"""
        try:
            # Add scheduled jobs
            self.scheduler.add_job(
                "morning_monitor",
                "0 9 * * *",  # 09:00 every day
                self.monitor_tasks
            )
            
            self.scheduler.add_job(
                "afternoon_monitor",
                "0 14 * * *",  # 14:00 every day
                self.monitor_tasks
            )
            
            self.scheduler.add_job(
                "evening_monitor",
                "0 20 * * *",  # 20:00 every day
                self.monitor_tasks
            )
            
            # Start scheduler
            self.scheduler.start()
            
            return {
                "status": "success",
                "message": "Task monitoring started successfully",
                "scheduled_jobs": self.scheduler.list_jobs()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to start monitoring: {str(e)}",
                "scheduled_jobs": []
            }
    
    def stop_monitoring(self):
        """Stop scheduled monitoring"""
        try:
            self.scheduler.stop()
            return {
                "status": "success",
                "message": "Task monitoring stopped successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to stop monitoring: {str(e)}"
            }

if __name__ == "__main__":
    # For testing
    import sys
    monitor = TaskMonitorSkill()
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "monitor":
            result = monitor.monitor_tasks()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif action == "start":
            result = monitor.start_monitoring()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif action == "stop":
            result = monitor.stop_monitoring()
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Usage: python monitor.py [monitor|start|stop]")
