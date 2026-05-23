# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from apscheduler.schedulers.background import BackgroundScheduler
# from contextlib import asynccontextmanager
# import pytz

# from app.graph import graph
# from app.linkedin import post_to_linkedin

# load_dotenv()

# def automated_linkedin_job():
#     """The function that runs automatically to generate and post."""
#     print("Triggering automated LinkedIn content generation...")
#     try:
#         # 1. Generate the post automatically (Analyst -> Research -> Write -> Review)
#         result = graph.invoke({})
#         final_post = result["final_post"]
        
#         # 2. Automatically publish it to LinkedIn without approval
#         response = post_to_linkedin(final_post)
#         print(f"Successfully posted to LinkedIn! Post ID: {response.get('post_id')}")
        
#     except Exception as e:
#         print(f"Scheduled job failed: {e}")

# # Manage the lifecycle of the FastAPI app to safely start/stop the scheduler
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Set this to the timezone of your target audience (e.g., "America/New_York", "Europe/London", or "Asia/Kolkata")
#     audience_timezone = pytz.timezone("Asia/Kolkata") 
#     scheduler = BackgroundScheduler(timezone=audience_timezone)
    
#     # Define the 5 optimal posting times
#     schedule_times = [
#         {"hour": 8, "minute": 30},   
#         {"hour": 10, "minute": 30},  
#         {"hour": 13, "minute": 0},   
#         {"hour": 16, "minute": 0},   
#         {"hour": 18, "minute": 30}   
#     ]
    
#     # Add a cron job for each time
#     for t in schedule_times:
#         scheduler.add_job(
#             automated_linkedin_job, 
#             trigger='cron', 
#             hour=t["hour"], 
#             minute=t["minute"]
#         )
        
#     scheduler.start()
#     print("Scheduler started. Waiting for next posting window...")
    
#     yield # App is running
    
#     scheduler.shutdown()
#     print("Scheduler gracefully shut down.")

# app = FastAPI(lifespan=lifespan)

# @app.get("/")
# def home():
#     return {"status": "Automated LinkedIn Agent is active and scheduling posts."}

# # Keeping this just in case you ever want to trigger a manual post
# class PublishRequest(BaseModel):
#     text: str

# @app.post("/publish-manual")
# def publish_manual(request: PublishRequest):
#     try:
#         response = post_to_linkedin(request.text)
#         return {"message": "Successfully posted manually", "linkedin_response": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))