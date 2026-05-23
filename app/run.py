# run.py
from dotenv import load_dotenv
from app.graph import graph
from app.linkedin import post_to_linkedin

load_dotenv()

def generate_and_post():
    print("Starting automated LinkedIn content generation...")
    try:
        # 1. Generate the post automatically (Analyst -> Research -> Write -> Review)
        result = graph.invoke({})
        final_post = result["final_post"]
        
        # 2. Automatically publish it to LinkedIn
        response = post_to_linkedin(final_post)
        print(f"Successfully posted to LinkedIn! Response: {response}")
        
    except Exception as e:
        print(f"Job failed: {e}")

if __name__ == "__main__":
    generate_and_post()