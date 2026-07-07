import sys
from Tools.news_tool import get_disaster_news, NewsToolError

class NewsAgent:

    def analyze(self, location: str) -> dict:
        """
        Analyzes disaster news articles for the given location.
        Scores each article for relevance to disasters, filtering out unrelated political,
        economic, sports, and general crime news.
        """
        try:
            news = get_disaster_news(location)
            articles = news.get("articles", [])
            
            scored_articles = []
            
            # 1. Target keyword sets
            disaster_keywords = [
                "flood", "deluge", "inundation", "cyclone", "hurricane", "typhoon", "storm",
                "earthquake", "quake", "tremor", "landslide", "mudslide", "wildfire", "bushfire",
                "forest fire", "evacuation", "evacuate", "relief", "rescue", "disaster", 
                "tsunami", "avalanche", "tornado", "casualty", "refugee", "shelter"
            ]
            
            exclusion_keywords = [
                "election", "vote", "campaign", "minister", "parliament", "congress", "senate",
                "stocks", "shares", "crypto", "bitcoin", "earnings", "profit", "merger", "acquisition",
                "celebrity", "actor", "hollywood", "movie", "album", "gossip", "divorce",
                "cricket", "football", "soccer", "championship", "tournament", "match",
                "theft", "robbery", "arrested for", "murder", "fraud", "corruption"
            ]
            
            for article in articles:
                if not isinstance(article, dict) or "title" not in article:
                    continue
                
                title = article["title"].lower()
                desc = (article.get("description") or "").lower()
                combined_text = title + " " + desc
                
                score = 0
                
                # Check for positive disaster indicators (+2 per match)
                for term in disaster_keywords:
                    if term in combined_text:
                        score += 2
                        
                # Check for location context match (+1 point)
                if location.lower() in combined_text:
                    score += 1
                    
                # Penalize unrelated topics (-5 points)
                for term in exclusion_keywords:
                    if term in combined_text:
                        score -= 5
                        
                # Keep articles passing a minimum threshold of relevance
                if score >= 2:  # Must have at least one disaster keyword or combinations
                    scored_articles.append((score, article))
            
            # Sort by relevance score in descending order
            scored_articles.sort(key=lambda x: x[0], reverse=True)
            
            # Extract metadata and top 5 relevant headlines
            articles_metadata = []
            for score, art in scored_articles[:5]:
                source_name = art.get("source", {}).get("name") or "Unknown Source"
                pub_date = art.get("publishedAt", "Date unavailable")
                if pub_date and "T" in pub_date:
                    pub_date = pub_date.split("T")[0]
                    
                articles_metadata.append({
                    "title": art["title"],
                    "source": source_name,
                    "date": pub_date,
                    "url": art.get("url", "#")
                })
            
            return {
                "location": location,
                "headlines": [a["title"] for a in articles_metadata],
                "articles": articles_metadata,
                "article_count": len(articles_metadata),
                "is_fallback": False
            }
            
        except NewsToolError as e:
            print(f"⚠️ Warning (NewsAgent): {e}. Using fallback empty news profile.", file=sys.stderr)
            return {
                "location": location,
                "headlines": [],
                "articles": [],
                "article_count": 0,
                "is_fallback": True,
                "error_message": str(e)
            }