from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class AppConfig:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_MODEL_ID = os.getenv("GOOGLE_MODEL_ID")
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

def validate_config():
    missing = []
    if not AppConfig.GOOGLE_API_KEY:
        missing.append("GOOGLE_API_KEY")
    if not AppConfig.GOOGLE_MODEL_ID:
        missing.append("GOOGLE_MODEL_ID")
    
    if missing:
        raise ValueError(f"Missing environment variables: {missing}")
    
validate_config()