from apscheduler.schedulers.background import BackgroundScheduler
from app.db.session import SessionLocal



scheduler = BackgroundScheduler()

def start_scheduler():
    def job():
        db = SessionLocal()
        try:
            deleted_count = cleanup_archived_tasks(db)
            print(f"[Scheduler] Deleted {deleted_count} expired tasks")
        finally:
            db.close()

    scheduler.add_job(job, "interval", hours=6)
    scheduler.start()




# This function deletes tasks that have been archived for more than 30 days

