from Tools.news_tool import get_disaster_news


class NewsAgent:

    def analyze(self, location):

        news = get_disaster_news(location)

        articles = news.get("articles", [])

        headlines = []

        for article in articles:
            headlines.append(article["title"])
        article_count = len(headlines)

        return {
            "location": location,
            "headlines": headlines,
           "article_count": article_count
        }