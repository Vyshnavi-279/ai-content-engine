import os
from pathlib import Path
from dotenv import load_dotenv
from runwayml import RunwayML

# Load .env from the directory where this config.py lives, so it works
# regardless of the current working directory.
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# 1. OpenRouter Configuration (Text Generation)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# Updated to a highly stable, current model slug to fix the 404 error
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct")

# 2. RunwayML Configuration (Visual Media Generation)
RUNWAYML_API_KEY = os.getenv("RUNWAY_API_KEY") or os.getenv("RUNWAYML_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("Missing OpenRouter API key for text generation.")

# Initialize the Runway client safely when an API key is available
rw = RunwayML(api_key=RUNWAYML_API_KEY) if RUNWAYML_API_KEY else None