import json
import requests
import time
import re

with open("cred.json","r") as file:
    GROQ_API_KEY = json.load(file)["GROQ_API_KEY"]
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def extract_json_block(text):
    # Extract JSON block from Markdown-style response
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    # Fallback: try to find any JSON-looking block
    match = re.search(r"(\{.*?\})", text, re.DOTALL)
    return match.group(1) if match else None

def enrich_article(summary):
    prompt = f"""
You are a cybersecurity assistant. Given the following threat article summary, extract actionable insights relevant to preventing attacks.

Rules:
1. If the summary is an advertisement, return exactly:
{{
  "Ad": true
}}

2. If the summary is actual news, return a JSON object with the following fields:
  "Alert": a good name for the alert generated from this news which expresses the relevent threats expressed
- "Mitre Tactics": an array of strings containing only these official MITRE ATT&CK tactic names:
  ["Reconnaissance","Resource Development","Initial Access","Execution","Persistence","Privilege Escalation",
   "Defense Evasion","Credential Access","Discovery","Lateral Movement","Collection","Command and Control",
   "Exfiltration","Impact"]
- "Mitre Techniques": an array of strings containing only MITRE ATT&CK technique codes (e.g., "T1059.001", "T1566").
- "Mitigation Suggestions": an array of strings with clear, actionable steps.
- "relevant_devices": an array of strings chosen only from this fixed list:
  ["email server", "Router/Firewall", "file Server", "ISP", "PC"]

Summary:
\"\"\"
{summary}
\"\"\"

Output requirements:
- Respond ONLY in valid JSON.
- Use the exact field names provided.
- Do not include comments, explanations, or extra text outside the JSON.
- Ensure the JSON is syntactically valid and will not cause JSONDecodeError.
"""



    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload)
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        try:
            return json.loads(extract_json_block(content))
        except json.JSONDecodeError:
            print("⚠️ Could not parse response as JSON:")
            print(content)
            return {}

# Load threat DB
with open("threat_db.json") as f:
    articles = json.load(f)

# Enrich each article
for article in articles:
    if all(k not in article for k in ["attack_vectors", "defensive_measures", "mitre_tactics", "relevant_devices"]):
        print(f"🔍 Enriching: {article['title']}")
        insights = enrich_article(article["summary"])
        if insights.get("Ad",False):
            continue
        else:
            article.update(insights)
        time.sleep(1.5)  # Respectful pacing

# Save enriched DB
with open("threat_db.json", "w") as f:
    json.dump(articles, f, indent=2)

print(f"\n✅ Enriched {len(articles)} articles with actionable insights.")

