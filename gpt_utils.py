import os
import requests

AZURE_OPENAI_ENDPOINT = "https://fy26-hackon-q1.openai.azure.com/openai/deployments/RazorSharkAI/chat/completions?api-version=2025-01-01-preview"
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

def call_gpt(messages, temperature=0.5):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY
    }
    payload = {
        "messages": messages,
        "temperature": temperature
    }

    try:
        response = requests.post(AZURE_OPENAI_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

def generate_subvention_split(row, brand):
    prompt = f"""
Brand: {brand}
Model: {row.get('Model', '')}
Cashback: {row.get('Cashback', '')}
Min Swipe Amount: {row.get('Min', '')}
Tenure: {row.get('Tenure', '')}
Bank: {row.get('Issuer', '')}

Suggest:
- Subvention Type (Fixed or Percentage)
- Bank Subvention Value
- Brand Subvention Value
- Justification
"""
    messages = [
        {"role": "system", "content": "You're a fintech offer expert who recommends smart subvention splits."},
        {"role": "user", "content": prompt}
    ]
    return call_gpt(messages)

def generate_offer_details(row, brand, field="name"):
    task = {
        "name": "Generate offer title",
        "desc": "Generate a short description for the offer",
        "cta": "Suggest a CTA like 'Shop Now' or 'Get ₹2000 Cashback'"
    }.get(field, "Generate offer title")

    prompt = f"""
{task} based on:
Brand: {brand}
Model: {row.get('Model', '')}
Cashback: {row.get('Cashback', '')}
Swipe: {row.get('Min', '')}
Tenure: {row.get('Tenure', '')}
Bank: {row.get('Issuer', '')}
Card Type: {row.get('Card Type', '')}
"""
    messages = [
        {"role": "system", "content": "You generate metadata for fintech offers."},
        {"role": "user", "content": prompt}
    ]
    return call_gpt(messages)

def generate_marketing_copy(row, brand, type="title"):
    task_map = {
        "title": "Generate a push notification title",
        "desc": "Generate a 1-line description",
        "tnc": "Generate short terms and conditions"
    }
    prompt = f"""
{task_map.get(type)} for:
Brand: {brand}
Model: {row.get('Model', '')}
Cashback: {row.get('Cashback', '')}
Tenure: {row.get('Tenure', '')}
Swipe: {row.get('Min', '')}
Bank: {row.get('Issuer', '')}
"""
    messages = [
        {"role": "system", "content": "You write short, catchy fintech marketing copy."},
        {"role": "user", "content": prompt}
    ]
    return call_gpt(messages)

def detect_anomalies(row):
    try:
        swipe = float(row.get("Min", 0))
        cashback = float(row.get("Cashback", 0))
        if cashback > 0.25 * swipe:
            return "⚠️ High Cashback"
        elif not row.get("Issuer") or not row.get("Tenure"):
            return "⚠️ Missing Key Fields"
        return "✅"
    except:
        return "⚠️ Error in validation"

def generate_full_offer_from_text(prompt_text):
    messages = [
        {"role": "system", "content": "You create full offer construct rows in structured format."},
        {"role": "user", "content": prompt_text}
    ]
    return call_gpt(messages)

 def generate_offer_construct(parsed_data, brand_name):
    # Dummy implementation, update with real Azure OpenAI logic
    return [
        {
            "Brand": brand_name,
            "Model": row.get("Model", ""),
            "Bank": row.get("Bank", ""),
            "Tenure": row.get("Tenure", ""),
            "Interest": row.get("Interest", ""),
            "Subvention": row.get("Subvention", "")
        }
        for row in parsed_data
]

