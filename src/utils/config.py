import os
from dotenv import load_dotenv

def validate_config():
    """Validates that all required environment variables are set."""
    load_dotenv()
    
    required_vars = [
        'GOODREADS_API_KEY',
        'GOODREADS_USER_ID',
        'AIDER_MODEL',
        'AIDER_EDITOR_MODEL',
        'CHAT_MODEL'
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        return False, f"❌ Missing required environment variables: {', '.join(missing)}"
    
    return True, "✅ Configuration is valid."

def get_config(key, default=None):
    """Safely get a configuration value."""
    return os.getenv(key, default)
