import os
from dotenv import load_dotenv
import yaml

load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Model config
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096

# Schedule
SEND_DAY = "monday"
SEND_TIME = "07:00"

def load_industries():
    """Load industry config from YAML"""
    config_path = os.path.join(os.path.dirname(__file__), "industries.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)["industries"]