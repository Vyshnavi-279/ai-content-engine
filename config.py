from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
OPENROUTER_MODEL = "openai/gpt-4o"

