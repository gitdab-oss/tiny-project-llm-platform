"""
Configuration file for Multi-LLM Chatbot
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

# Model configurations
MODELS = {
    "openai": {
        "default": "gpt-4",
        "api_key_env": "OPENAI_API_KEY"
    },
    "llama": {
        "default": "llama-3.3-70b-versatile",
        "api_key_env": "GROQ_API_KEY"
    },
    "gemini": {
        "default": "gemini-2.5-flash",
        "api_key_env": "GOOGLE_API_KEY"
    }
}

# API endpoint configurations
API_CONFIG = {
    "timeout": 30,  # seconds
    "max_retries": 3,
    "temperature": 0.7,
    "max_tokens": 1024
}

# UI Configuration
UI_CONFIG = {
    "show_token_usage": True,
    "show_response_time": True,
    "max_conversation_history": 20,  # messages
    "enable_streaming": False  # Future feature
}

