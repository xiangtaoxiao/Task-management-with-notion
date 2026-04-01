import schedule
import time
import threading
import logging

class SchedulerTool:
    def __init__(self):
        self.jobs = {}
        self.running = False
        self.thread = None
    
    def add_job(self, name, cron_expression, func, *args, **kwargs):
        """Add a job with cron expression"""
        # Convert cron expression to schedule format
        parts = cron_expression.split()
        if len(parts) != 5:
            raise ValueError("Invalid cron expression format")
        
        minute, hour, day, month, weekday = parts
        
        # Create schedule
        job = schedule.every()
        
        # Set weekday if specified
        if weekday != '*':
            weekdays = {
                '0': 'sunday',
                '1': 'monday',
                '2': 'tuesday',
                '3': 'wednesday',
                '4': 'thursday',
                '5': 'friday',
                '6': 'saturday'
            }
            if weekday in weekdays:
                job = getattr(job, weekdays[weekday])
        
        # Set month if specified
        if month != '*':
            # schedule library doesn't support month scheduling directly
            # We'll handle this in the job function
            pass
        
        # Set day if specified
        if day != '*':
            job = job.day
        
        # Set hour and minute
        job = job.at(f"{hour}:{minute}")
        
        # Schedule the job
        job_func = job.do(func, *args, **kwargs)
        self.jobs[name] = job_func
        logging.info(f"Added job {name} with cron {cron_expression}")
    
    def remove_job(self, name):
        """Remove a job by name"""
        if name in self.jobs:
            schedule.cancel_job(self.jobs[name])
            del self.jobs[name]
            logging.info(f"Removed job {name}")
    
    def start(self):
        """Start the scheduler"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.thread.start()
            logging.info("Scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        logging.info("Scheduler stopped")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def list_jobs(self):
        """List all scheduled jobs"""
        return list(self.jobs.keys())
