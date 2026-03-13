import requests
from datetime import datetime, timedelta
from config.settings import load_industries
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

def search_news(query: str) -> list[dict]:
    """Fetch recent news articles from NewsAPI"""
    today = datetime.now()
    week_ago = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    
    params = {
        "q": query,
        "from": week_ago,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }
    
    try:
        response = requests.get(NEWS_API_URL, params=params)
        data = response.json()
        
        results = []
        for article in data.get("articles", []):
            pub_date = article.get("publishedAt", "")
            pub_date = article.get("publishedAt", "")
            if not pub_date:
                continue
            parsed = datetime.strptime(pub_date[:10], "%Y-%m-%d")
            formatted_date = parsed.strftime("%b %d")
            
            results.append({
                "title": article.get("title", ""),
                "snippet": article.get("description", ""),
                "source": article.get("source", {}).get("name", ""),
                "date": formatted_date,
                "url": article.get("url", "")
            })
        
        return results
    except Exception as e:
        print(f"  NewsAPI error for '{query}': {e}")
        return []
def search_rss(query: str) -> list[dict]:
    """Fetch fresh news from Google News RSS"""
    try:
        encoded_query = requests.utils.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
        
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        
        from xml.etree import ElementTree as ET
        root = ET.fromstring(response.content)
        
        results = []
        for item in root.findall(".//item")[:5]:
            title = item.findtext("title", "")
            snippet = item.findtext("description", "")
            pub_date_raw = item.findtext("pubDate", "")
            source_tag = item.find("source")
            source = source_tag.text if source_tag is not None else "Google News"
            
            if pub_date_raw:
                try:
                    from email.utils import parsedate_to_datetime
                    parsed = parsedate_to_datetime(pub_date_raw)
                    formatted_date = parsed.strftime("%b %d")
                except:
                    formatted_date = ""
            else:
                formatted_date = ""
            
            if not formatted_date:
                continue
                
            results.append({
                "title": title,
                "snippet": snippet,
                "source": source,
                "date": formatted_date,
                "url": ""
            })
        
        return results
    except Exception as e:
        print(f"  RSS error for '{query}': {e}")
        return []
    
def research_industries() -> list[dict]:
    """Research all configured industries"""
    industries = load_industries()
    all_research = []
    today = datetime.now().strftime("%B %d, %Y")
    
    for industry in industries:
        print(f"  Researching {industry['name']}...")
        industry_research = {
            "industry": industry["name"],
            "as_of_date": today,
            "findings": []
        }
        
        for keyword in industry["keywords"]:
            # NewsAPI for depth
            news_results = search_news(keyword)
            industry_research["findings"].extend(news_results)
            # RSS for freshness
            rss_results = search_rss(keyword)
            industry_research["findings"].extend(rss_results)
        
        for company in industry.get("companies", []):
            news_results = search_news(f"{company} cruise")
            industry_research["findings"].extend(news_results)
            rss_results = search_rss(f"{company} cruise")
            industry_research["findings"].extend(rss_results)
        
        # Deduplicate by title
        seen = set()
        unique_findings = []
        for f in industry_research["findings"]:
            if f["title"] not in seen:
                seen.add(f["title"])
                unique_findings.append(f)
        
        industry_research["findings"] = unique_findings
        all_research.append(industry_research)
    
    return all_research