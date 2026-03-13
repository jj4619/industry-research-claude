from agent.researcher import research_industries
from agent.synthesizer import synthesize_briefing
from agent.emailer import send_briefing
from datetime import datetime, timedelta

def run_briefing():
    print("Starting weekly industry briefing...")
    
    next_monday = (datetime.now() + timedelta(days=(7 - datetime.now().weekday()))).strftime("Mon %b %d, %Y")

    print("Researching industries...")
    raw_research = research_industries()

    print("Synthesizing insights...")
    briefing = synthesize_briefing(raw_research)

    briefing["week_of"] = datetime.now().strftime("%b %d, %Y")
    briefing["next_briefing"] = next_monday
    briefing["industry"] = raw_research[0]["industry"]
    briefing["signals_tracked"] = len(raw_research[0]["findings"])

    print("Sending email...")
    send_briefing(briefing)

    print("Done! Briefing sent successfully.")

if __name__ == "__main__":
    run_briefing()