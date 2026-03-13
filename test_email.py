import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import os

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

dummy_briefing = {
    "industry": "Cruise Industry",
    "week_of": "Mar 10, 2026",
    "signals_tracked": 24,
    "brand_color": "#003087",
    "accent_color": "#0077C8",
    "next_briefing": "Mon Mar 17, 2026",
    "market": {
        "rcl_price": "$162.40",
        "rcl_change": "+3.2%",
        "rcl_direction": "up",
        "sp500_change": "+1.1%",
        "sp500_direction": "up",
        "crude_change": "-2.4%",
        "crude_direction": "down",
        "crude_price": "$74.10"
    },
    "executive_summary": [
        "Royal Caribbean reports record Q1 bookings driven by private destination demand",
        "Carnival margins under pressure as fuel hedging contracts expire mid-year",
        "MSC Cruises accelerating North America expansion — direct competitive threat to RCL",
        "New EU emissions regulations effective 2027 forcing fleet retrofit decisions now",
        "Shore excursion revenue emerging as next yield battleground across all major lines"
    ],
    "industry_pulse": [
        "Royal Caribbean breaks ground on second Perfect Day destination in Bahamas",
        "Carnival Corporation sells two older vessels to fund newbuild program",
        "Norwegian announces $2B refinancing at favorable rates"
    ],
    "competitive_signals": [
        "MSC hiring 200+ North America sales roles — aggressive distribution push",
        "Virgin Voyages expanding to Caribbean year-round from 2027",
        "Disney Cruise Line ordering two new ships for Asian deployment"
    ],
    "macro_forces": [
        "Consumer travel spend remains resilient despite broader discretionary softness",
        "Fuel costs stabilizing — tailwind for margin recovery in H2",
        "China outbound travel recovery accelerating — Asia itineraries filling fast"
    ],
    "bd_opportunities": [
        "Carnival operational restructuring — cost transformation opportunity",
        "Norwegian integrating recent acquisition — integration support play",
        "Several mid-tier lines facing yield management capability gaps"
    ],
    "big_idea": "Private destinations are quietly becoming the most important strategic asset in cruise — Royal Caribbean's Perfect Day generates 2x the onboard revenue of a port day. The lines that own their destinations will structurally outcompete those that don't. This is a 10-year moat being built right now."
}

template_dir = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("email_template.html")
html_content = template.render(briefing=dummy_briefing)

msg = MIMEMultipart("alternative")
msg["Subject"] = "Weekly Cruise Industry Briefing — Mar 12, 2026"
msg["From"] = GMAIL_ADDRESS
msg["To"] = RECIPIENT_EMAIL

msg.attach(MIMEText(html_content, "html"))

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
    print("Success! Check your inbox.")
except Exception as e:
    print(f"Error: {e}")