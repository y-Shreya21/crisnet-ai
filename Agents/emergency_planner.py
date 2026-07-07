class EmergencyPlanner:
    """
    Emergency Planning Agent.
    Generates action recommendations and safety protocols based on assessed threat severity levels.
    """

    def generate_plan(self, risk: dict) -> list:
        """
        Generates tactical action list tailored to the assessed risk severity.
        """
        severity = risk.get("severity", "LOW")

        if severity == "CRITICAL":
            return [
                "URGENT: Initiate mandatory mass evacuations immediately!",
                "Establish temporary incident command posts and relief distribution points",
                "Deploy rapid search and rescue units alongside national emergency reserves",
                "Establish dedicated air-evacuation corridors if surface paths are blocked",
                "Broadcast critical alerts and assembly warnings continuously via all channels"
            ]

        elif severity == "HIGH":
            return [
                "Activate emergency shelters immediately",
                "Deploy rescue and medical teams",
                "Issue evacuation alerts",
                "Stock emergency supplies",
                "Monitor weather conditions continuously"
            ]

        elif severity == "MEDIUM":
            return [
                "Prepare emergency shelters",
                "Alert local authorities",
                "Monitor affected regions",
                "Keep rescue teams on standby"
            ]

        else:
            return [
                "Continue routine monitoring",
                "Maintain communication channels"
            ]