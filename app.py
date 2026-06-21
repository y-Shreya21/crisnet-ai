from coordinator import CoordinatorAgent

agent = CoordinatorAgent()

result = agent.process(
    "Assam",
    26.1445,
    91.7362
)

print(result)

print("\n🚨 CRISISNET RISK ASSESSMENT REPORT")
print(f"\nLocation: Assam")

print(f"\nRisk Score: {result['risk']['risk_score']}/10")
print(f"Severity: {result['risk']['severity']}")

print(f"\nHumidity: {result['weather']['humidity']}%")
print(f"Precipitation: {result['weather']['precipitation']} mm")

print(f"\nRelevant News Articles: {result['news']['article_count']}")