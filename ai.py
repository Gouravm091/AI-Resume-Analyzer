from google import genai
from dotenv import load_dotenv
import json
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def analyze_resume(resume_text, user_goal):
    prompt = f"""
    You are a senior software engineer and hiring manager.
    
    Evaluate the resume based on the user's goal.
    
    User's Target Role:
    {user_goal}

    Resume:
    {resume_text}
    
    STRICT RULES:
    - Extract only relevant skills for this goal 
    - REMOVE irrelevant tools [excel for backend, etc]
    - Identify real gaps
    - Generate roadmap only for missing fields
    - Make output DIFFERENT based on goal
    
    Return only JSON:
    {{
    "skills":[],
    "missing_skills":[],
    "roadmap": [],
    "interview_questions": []
    
    }}
    
    """
    try:
        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )
        
        content = response.output_text.strip()
        
        start = content.find("{")
        end = content.rfind("}")+1
        
        return json.loads(content[start:end])
    
    except Exception as e:
        return {
            "skills":[],
            "missing_skills":[],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }