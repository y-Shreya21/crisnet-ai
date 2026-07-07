class AlertAgent:
    """
    Alert Agent monitors the severity score and formulates standardized public warning notifications.
    """

    def generate_alert(self, risk_score: float, severity: str, disaster_type: str) -> dict:
        """
        Builds threat alert headers, colors, and broadcast messages.
        """
        sev = severity.upper()
        dtype = disaster_type.upper() if disaster_type else "DISASTER"

        if sev == "CRITICAL":
            color_hex = "#ff0000"
            level = "CRITICAL"
            headline = f"🔴 CRITICAL {dtype} WARNING"
            message = (
                f"Severe {disaster_type.lower()} conditions detected. "
                "Immediate evacuation may be required. Move to designated shelters. "
                "Avoid low-lying areas. Turn off main utility lines (gas/power)."
            )
        elif sev == "HIGH":
            color_hex = "#ff4b4b"
            level = "HIGH"
            headline = f"🟠 HIGH {dtype} WARNING"
            message = (
                f"Significant {disaster_type.lower()} conditions building. "
                "Relocate vulnerable individuals to safe zones. "
                "Stay indoors and prepare emergency kits. Monitor official reports."
            )
        elif sev == "MEDIUM" or sev == "MODERATE":
            color_hex = "#ffaf5e"
            level = "MODERATE"
            headline = f"🟡 MODERATE {dtype} ALERT"
            message = (
                f"Active {disaster_type.lower()} activity reported. "
                "Secure loose items outdoors, check battery radios, and "
                "keep emergency contact lists available."
            )
        else:
            color_hex = "#48bb78"
            level = "LOW"
            headline = f"🟢 LOW {dtype} MONITORING"
            message = (
                f"No immediate threat from {disaster_type.lower()} conditions. "
                "Maintain baseline situational awareness and readiness."
            )

        return {
            "level": level,
            "color": color_hex,
            "headline": headline,
            "message": message,
            "risk_score": risk_score
        }
