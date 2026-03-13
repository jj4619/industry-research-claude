import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from config.settings import GMAIL_ADDRESS, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL
import os

def render_email(briefing: dict) -> str:
    """Render briefing dict into HTML email"""
    template_dir = os.path.join(os.path.dirname(__file__), "../templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("email_template.html")
    return template.render(briefing=briefing)

def save_to_docs(html_content: str):
    """Save rendered HTML to docs/index.html for GitHub Pages"""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        docs_dir = os.path.join(base_dir, "docs")
        docs_path = os.path.join(docs_dir, "index.html")
        
        print(f"  Saving to: {docs_path}")
        
        os.makedirs(docs_dir, exist_ok=True)
        
        with open(docs_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        size = os.path.getsize(docs_path)
        print(f"  Saved successfully — {size} bytes written")
        
    except Exception as e:
        print(f"  ERROR saving to docs: {e}")

def send_briefing(briefing: dict):
    """Send rendered briefing via Gmail"""
    html_content = render_email(briefing)
    
    save_to_docs(html_content)
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Weekly Industry Briefing"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    
    msg.attach(MIMEText(html_content, "html"))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())