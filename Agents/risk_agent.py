class RiskAgent:
    """
    Intelligent Risk Assessment Agent.
    Calculates multi-factor risk index evaluating weather hazards,
    disaster news severity, and resource scarcity vulnerabilities.
    """

    def analyze(self, weather_data: dict, news_data: dict, resource_data: dict = None) -> dict:
        """
        Calculates a risk score between 0.0 and 10.0 and classifies severity level.
        Generates explainable natural language reasoning for emergency responders.
        """
        risk_score = 0.0
        reasons = []

        # 1. Weather Threat Factors (Max 5.0 points)
        precipitation = weather_data.get("precipitation", 0.0)
        humidity = weather_data.get("humidity", 50)
        wind_speed = weather_data.get("wind_speed", 0.0)

        # Precipitation factor (Rainfall and flash flooding risk)
        if precipitation >= 50.0:
            risk_score += 2.5
            reasons.append(f"extreme precipitation ({precipitation} mm)")
        elif precipitation >= 20.0:
            risk_score += 1.8
            reasons.append(f"heavy rainfall ({precipitation} mm)")
        elif precipitation > 0.0:
            risk_score += 1.0
            reasons.append(f"precipitation detected ({precipitation} mm)")

        # Wind speed factor (Storm / Cyclone risk)
        if wind_speed >= 25.0:
            risk_score += 1.5
            reasons.append(f"severe storm wind speeds ({wind_speed} m/s)")
        elif wind_speed >= 15.0:
            risk_score += 1.0
            reasons.append(f"high winds ({wind_speed} m/s)")
        elif wind_speed >= 8.0:
            risk_score += 0.5
            reasons.append(f"moderate breeze ({wind_speed} m/s)")

        # Humidity factor
        if humidity > 90:
            risk_score += 1.0
            reasons.append("extremely high humidity (above 90%)")
        elif humidity > 80:
            risk_score += 0.5
            reasons.append("elevated humidity (above 80%)")

        # 2. News Alert Factors (Max 3.0 points)
        article_count = news_data.get("article_count", 0)
        if article_count >= 5:
            risk_score += 3.0
            reasons.append(f"high volume of active disaster reports ({article_count} reports)")
        elif article_count >= 3:
            risk_score += 2.0
            reasons.append(f"multiple active disaster reports ({article_count} reports)")
        elif article_count >= 1:
            risk_score += 1.0
            reasons.append("active disaster report published")

        # 3. Vulnerability / Resource Scarcity Factors (Max 2.0 points)
        if resource_data:
            hospitals = resource_data.get("hospital_count", 0)
            shelters = resource_data.get("shelter_count", 0)

            # Scarcity of hospitals increases threat to life/casualties handling
            if hospitals == 0:
                risk_score += 1.0
                reasons.append("critical hospital scarcity (0 found)")
            elif hospitals < 3:
                risk_score += 0.5
                reasons.append(f"scarce hospital infrastructure ({hospitals} found)")

            # Scarcity of emergency shelters limits displacement safety
            if shelters == 0:
                risk_score += 1.0
                reasons.append("critical shelter scarcity (0 found)")
            elif shelters < 2:
                risk_score += 0.5
                reasons.append(f"limited shelter availability ({shelters} found)")

        # Cap overall threat index to 10.0 and round
        risk_score = round(min(risk_score, 10.0), 2)

        # 4. Severity Classification
        if risk_score <= 3.0:
            severity = "LOW"
        elif risk_score <= 6.0:
            severity = "MEDIUM"
        elif risk_score <= 8.5:
            severity = "HIGH"
        else:
            severity = "CRITICAL"

        # 5. Formulate explainable reasoning statement
        if not reasons:
            reasoning = "Normal environmental parameters and no active hazard reports."
        else:
            # Capitalize first letter of explanation
            reason_str = ", ".join(reasons)
            reasoning = f"Threat level elevated due to: {reason_str}."

        return {
            "risk_score": risk_score,
            "severity": severity,
            "reasoning": reasoning
        }