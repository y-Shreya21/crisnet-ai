import sys
from dotenv import load_dotenv
load_dotenv()
from Agents.coordinator import CoordinatorAgent

agent = CoordinatorAgent()

print("🚨 CRISISNET AI: INCIDENT OPERATIONS DISPATCH")
print("=" * 50)

location = input("Enter Incident Location Name [Assam]: ").strip() or "Assam"
print("\n🌐 Available Languages: en, hi, pa, ta, te, bn, mr, gu, kn, ml, ur")
lang_code = input("Select Language Code [en]: ").strip() or "en"

try:
    # process resolves coordinates automatically using LocationAgent internally (Phase 0)
    result = agent.process(location, target_language=lang_code)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

loc_res = result["resolved_location"]

print("\n🚨 CRISISNET AI DISASTER RESPONSE REPORT")
print("=" * 40)
print(f"📍 Resolved Location: {loc_res['name']}, {loc_res['country']}")
print(f"📍 Coordinates: Latitude {loc_res['latitude']} | Longitude {loc_res['longitude']}")
if loc_res.get("is_fallback"):
    print("  (⚠️ Using fallback coordinates due to geocoding API offline)")
print(f"Risk Level: {result['risk']['severity']}")
print(f"Risk Score: {result['risk']['risk_score']}/10")

print("\n🌦️ Weather Indicators:")
print(f"• Temperature: {result['weather']['temperature']}°C")
print(f"• Humidity: {result['weather']['humidity']}%")
print(f"• Precipitation: {result['weather']['precipitation']} mm")
print(f"• Wind Speed: {result['weather']['wind_speed']} m/s")
if result['weather'].get('is_fallback'):
    print("  (⚠️ Using fallback weather data due to API error)")

print(f"\n📰 Relevant News: {result['news']['article_count']} articles found")
if result['news']['headlines']:
    for headline in result['news']['headlines']:
        print(f"• {headline}")
if result['news'].get('is_fallback'):
    print("  (⚠️ Using fallback news data due to API error)")

print("\n📋 Available Resources:")
print(f"• Shelters: {result['resources']['shelter_count']}")
print(f"• Hospitals: {result['resources']['hospital_count']}")
print(f"• Fire Stations: {result['resources']['fire_station_count']}")

print(f"\n📢 Broadcast Warning:")
print(f"[{result['alert']['level']}] {result['alert']['headline']}")
print(f"• Info: {result['alert']['message']}")

print("\n📞 Local Emergency Contacts:")
contacts = result["emergency_contacts"]
print("• Police: [REDACTED]")
print("• Ambulance: [REDACTED]")
print("• Fire Services: [REDACTED]")
print("• Disaster Helpline: [REDACTED]")
print("• Nearest Hospital: [REDACTED]")

print("\n📋 Citizen Safety Guidance:")
guidance = result["safety_guidance"]
print(f"[{guidance['type']}]")
print("Immediate Actions Right Now:")
for action in guidance["immediate_actions"]:
    print(f"  ✓ {action}")
print("Evacuation Instructions:")
for evac in guidance["evacuation_instructions"]:
    print(f"  ✓ {evac}")

print("\n📢 Recommended Actions:")
for idx, action in enumerate(result["plan"], start=1):
    print(f"{idx}. {action}")
print("=" * 40)