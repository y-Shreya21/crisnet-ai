class EmergencyPlanner:

    def generate_plan(
        self,
        weather,
        news,
        resources,
        risk
    ):

        return f"""
DISASTER RESPONSE REPORT

Risk Level: {risk['severity']}
Risk Score: {risk['risk_score']}

Affected Areas:
{news['affected_areas']}

Recommended Actions:
1. Open emergency shelters
2. Deploy rescue teams
3. Issue evacuation alerts
4. Stock medical supplies
5. Monitor weather continuously
"""
class EmergencyPlanner:

    def generate_plan(
        self,
        weather,
        news,
        resources,
        risk
    ):

        return f"""
DISASTER RESPONSE REPORT

Risk Level: {risk['severity']}
Risk Score: {risk['risk_score']}

Affected Areas:
{news['affected_areas']}

Recommended Actions:
1. Open emergency shelters
2. Deploy rescue teams
3. Issue evacuation alerts
4. Stock medical supplies
5. Monitor weather continuously
"""