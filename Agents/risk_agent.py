class RiskAgent:

    def analyze(self, weather_data, news_data):

        risk_score = 0

        # Weather Factors
        if weather_data["humidity"] > 80:
            risk_score += 2

        if weather_data["precipitation"] > 0:
            risk_score += 3

        if weather_data["wind_speed"] > 20:
            risk_score += 2

        # News Factors
        article_count = news_data["article_count"]

        if article_count >= 3:
            risk_score += 2

        if article_count >= 5:
            risk_score += 1

        # Severity Classification
        if risk_score <= 3:
            severity = "LOW"

        elif risk_score <= 6:
            severity = "MEDIUM"

        else:
            severity = "HIGH"

        return {
            "risk_score": risk_score,
            "severity": severity
        }