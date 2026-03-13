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

def send_briefing(briefing: dict):
    """Send rendered briefing via Gmail"""
    html_content = render_email(briefing)
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Weekly Industry Briefing"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    
    msg.attach(MIMEText(html_content, "html"))
    docs_path = os.path.join(os.path.dirname(__file__), "../docs/index.html")
    with open(docs_path, "w") as f:
        f.write(html_content)
        
    print("  Briefing saved to docs/index.html")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())