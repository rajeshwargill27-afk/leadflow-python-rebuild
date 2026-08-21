import pandas as pd
import requests
import os

api_key = os.environ.get("ANTHROPIC_API_KEY")

# --- Step A: Load and tier leads (from Week 3) ---

def assign_tier(row):
    if row["industry"] == "Retailer":
        return "Tier 3"
    if row["company_size"] < 10:
        return "Tier 3"
    if row["geography"] not in ["USA", "Canada"]:
        return "Tier 3"
    if row["title"] == "Unknown":
        return "Tier 3"
    if row["source"] != "Apollo export":
        return "Tier 3"
    if row["industry"] == "Sofa manufacturer" and row["title"] in ["Owner", "CEO", "Procurement Manager"]:
        return "Tier 1"
    return "Tier 2"

df = pd.read_csv("leads2.csv")
df["tier"] = df.apply(assign_tier, axis=1)

tier1_leads = df[df["tier"] == "Tier 1"]
print(tier1_leads)

def draft_outreach(lead_name, industry):
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 150,
                "messages": [
                    {"role": "user", "content": f"Write a short, 2-sentence cold outreach email opener for {lead_name}, a {industry}. We are Furniture Arte — mention we make leather sofa covers with fast turnaround. Don't use a placeholder for our company name, use 'Furniture Arte' directly."}
                ]
            }
        )
        result = response.json()
        return result["content"][0]["text"]
    except Exception as e:
        print(f"Error drafting outreach for {lead_name}: {e}")
        return None
    
for index, row in tier1_leads.iterrows():
    outreach_copy = draft_outreach(row["name"], row["industry"])
    if outreach_copy:
        print(f"Lead: {row['name']}")
        print(f"Outreach: {outreach_copy}")
        print()
    # --- Step C: Simulate writing the tier back to HubSpot ---

def update_hubspot_contact(lead_name, tier):
    # In a real version, this would be:
    # requests.patch(f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}",
    #                 headers={"Authorization": f"Bearer {hubspot_api_key}"},
    #                 json={"properties": {"lead_tier": tier}})
    print(f"[SIMULATED HUBSPOT WRITE] Would update {lead_name} — set Lead Tier = {tier}")

for index, row in tier1_leads.iterrows():
    update_hubspot_contact(row["name"], row["tier"])