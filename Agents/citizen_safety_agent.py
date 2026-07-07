class CitizenSafetyAgent:
    """
    Citizen Safety Agent generates clear, disaster-specific, actionable 
    emergency guidelines for citizens during crisis events.
    """

    def generate_guidance(self, disaster_type: str) -> dict:
        """
        Returns structured lists of practical safety directives based on disaster type.
        """
        dtype = disaster_type.lower()

        if "flood" in dtype:
            return {
                "type": "FLOOD SAFETY PROTOCOLS",
                "immediate_actions": [
                    "Move immediately to higher ground; do not wait for instruction.",
                    "Avoid walking, swimming, or driving through flood waters.",
                    "If water rises in your building, move to the roof only if necessary.",
                    "Keep emergency kits, clean drinking water, and dry food packed."
                ],
                "evacuation_instructions": [
                    "Evacuate immediately if local authorities issue an order.",
                    "Turn off utilities (electricity and gas) before leaving.",
                    "Follow designated evacuation routes; do not take shortcuts."
                ],
                "what_to_avoid": [
                    "Avoid driving over flooded bridges or roads (most vehicle deaths occur here).",
                    "Do not touch electrical equipment if you are wet or standing in water."
                ]
            }

        elif "earthquake" in dtype:
            return {
                "type": "EARTHQUAKE SAFETY PROTOCOLS",
                "immediate_actions": [
                    "DROP down onto your hands and knees.",
                    "COVER your head and neck under sturdy furniture (desk/table).",
                    "HOLD ON to your shelter until the shaking stops.",
                    "If outdoors, move away from buildings, streetlights, and utility wires."
                ],
                "evacuation_instructions": [
                    "Do not use elevators; use stairwells after shaking stops.",
                    "Be prepared for aftershocks which can cause further damage.",
                    "Move to open public areas or parks away from high structures."
                ],
                "what_to_avoid": [
                    "Avoid standing near glass windows, heavy shelves, or outer walls.",
                    "Do not light matches or turn on gas switches (leakage risks)."
                ]
            }

        elif "cyclone" in dtype or "hurricane" in dtype or "typhoon" in dtype or "storm" in dtype:
            return {
                "type": "CYCLONE SAFETY PROTOCOLS",
                "immediate_actions": [
                    "Stay inside and keep all doors and windows securely locked.",
                    "Secure loose outdoor items (garbage cans, patio furniture) that could become projectiles.",
                    "Keep battery-powered radios tuned to official weather service alerts.",
                    "Store emergency drinking water in bathtubs or large containers."
                ],
                "evacuation_instructions": [
                    "Evacuate to designated cyclone shelters if your house is low-lying.",
                    "Unplug all electrical appliances to prevent damage from power surges."
                ],
                "what_to_avoid": [
                    "Do not go outside during the calm eye of the storm (winds will return suddenly).",
                    "Avoid low-lying coastal areas susceptible to storm surges."
                ]
            }

        elif "wildfire" in dtype or "fire" in dtype:
            return {
                "type": "WILDFIRE SAFETY PROTOCOLS",
                "immediate_actions": [
                    "Evacuate immediately if your area is under warning; do not wait.",
                    "Wear N95 masks or wrap wet cloth around your nose and mouth.",
                    "Close all windows, vents, and doors to prevent smoke penetration.",
                    "Pack dry emergency clothes, medications, and IDs in a go-bag."
                ],
                "evacuation_instructions": [
                    "Drive slowly with headlights on; be alert for emergency vehicles.",
                    "Follow routes designated by fire wardens; avoid smoke-heavy valleys."
                ],
                "what_to_avoid": [
                    "Do not attempt to defend property yourself if evacuation is ordered.",
                    "Avoid traveling down paths with dense foliage on both sides."
                ]
            }

        elif "landslide" in dtype or "mudslide" in dtype:
            return {
                "type": "LANDSLIDE SAFETY PROTOCOLS",
                "immediate_actions": [
                    "Stay alert for rumbling sounds, cracking trees, or moving boulders.",
                    "If near a stream, monitor any sudden increase or decrease in water flow.",
                    "Curl into a tight ball and protect your head if escape is impossible."
                ],
                "evacuation_instructions": [
                    "Evacuate rapidly if land movement is observed or suspected.",
                    "Warn neighbors and assist elderly/disabled individuals in surrounding structures."
                ],
                "what_to_avoid": [
                    "Avoid low-lying river valleys or channels where debris flows accumulate.",
                    "Do not return to the landslide site until official geologists verify safety."
                ]
            }

        else:
            return {
                "type": "GENERAL EMERGENCY SAFETY PROTOCOLS",
                "immediate_actions": [
                    "Keep emergency communication lines clear; monitor local broadcasts.",
                    "Ensure your emergency survival kit (water, food, radio, flashlight) is ready.",
                    "Check on family members and neighbors, especially vulnerable individuals."
                ],
                "evacuation_instructions": [
                    "Obey instructions from local wardens and response officials.",
                    "Follow safe transport maps to designated evacuation shelters."
                ],
                "what_to_avoid": [
                    "Avoid spreading unverified rumors or reports on social media.",
                    "Do not approach damaged electrical poles or fallen power lines."
                ]
            }
