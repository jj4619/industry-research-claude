import anthropic
from config.settings import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS
from agent.market_data import get_market_snapshot
from datetime import datetime

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def synthesize_briefing(research: list[dict]) -> dict:
    """Use Claude to synthesize research into consulting-grade briefing"""
    
    # Format research for prompt
    research_text = ""
    research_text = ""
    for industry in research:
        research_text += f"\n\nINDUSTRY: {industry['industry']}\n"
        for i, finding in enumerate(industry["findings"][:20]):
            research_text += f"\n[{i+1}] DATE: {finding.get('date', 'Recent')} | SOURCE: {finding.get('source', 'Unknown')}\nHEADLINE: {finding['title']}\nDETAIL: {finding['snippet']}\n"
    
    prompt = f"""You are a BCG consultant preparing a weekly industry briefing. Today is {datetime.now().strftime("%B %d, %Y")}.

Based on the following raw research, produce a structured briefing with these exact sections:

1. EXECUTIVE SUMMARY - 4-5 sharp "so what" bullets
2. INDUSTRY PULSE - Major moves, deals, shifts
3. COMPETITIVE SIGNALS - What key players are doing
4. MACRO FORCES - Broader tailwinds and headwinds
5. BD OPPORTUNITIES - Companies showing consulting need signals

CRITICAL RULES:
- Today is {datetime.now().strftime("%B %d, %Y")}
- Every bullet MUST start with "Mon DD (Source) —" using the exact DATE field e.g. "Mar 10 (Reuters) —"
- Use only the DATE field exactly as provided, never modify or fabricate it
- If no DATE is provided for a finding, skip it entirely
- Every bullet must include at least one specific number: %, $, or named figure
- Maximum 12 words per bullet after the date and source — ruthlessly cut everything else
- Think: "Mar 10 (Reuters) — RCL Q1 bookings +22% YoY, driven by private destinations"
- If it runs longer than 12 words, cut the least important words until it doesn't
- No explanations, no "this signals that..." commentary — just the fact

RAW RESEARCH (as of {datetime.now().strftime("%B %d, %Y")}):
{research_text}

Return pure JSON only, no markdown. Keys: executive_summary, industry_pulse, competitive_signals, macro_forces, bd_opportunities
All keys are lists of strings."""

    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}]
    )
    
    import json
    response_text = message.content[0].text
    
    # Clean JSON if wrapped in markdown
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0].strip()
    
    briefing = json.loads(response_text)
    briefing["market"] = get_market_snapshot()
    return briefing