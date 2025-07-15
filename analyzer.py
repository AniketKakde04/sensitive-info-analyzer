import os
import re
import json
from dotenv import load_dotenv
from encryption import encrypt_text
from vector_store import search_similar, add_example_to_vector_db
import google.generativeai as genai

# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.0-flash")

def analyze_text(text: str):
    masked_text = text
    log = []

    # Step 1: Search vector DB (RAG)
    results = search_similar(text, top_k=5)
    examples = [doc for doc in results["documents"][0]]

    print("\n🔎 RAG matched examples:")
    for ex in examples:
        print(f"  → {ex}")

    # Step 2: Gemini Prompt
    prompt = [
        "You're a data privacy detection system.",
        "Return ONLY a JSON array of sensitive values from the given message, such as:",
        "- PAN numbers (e.g. AXZP1234Q)",
        "- Aadhaar numbers (e.g. 1234 5678 9012)",
        "- Phone, email, UPI, account numbers, passport, IP address, etc.",
        "- Custom values like customer ID, reference number, ticket number, etc.",
        "No explanations. Only output a JSON array like [\"value1\", \"value2\"]",
        "",
        "Examples:",
        "Text: 'My PAN is AXZP1234Q' → [\"AXZP1234Q\"]",
        "Text: 'Aadhaar: 1234 5678 9012' → [\"1234 5678 9012\"]",
        "Text: 'My customer ID is XYN99882T' → [\"XYN99882T\"]",
        f"Text: {text}"
    ]

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        print("\n🧠 Gemini raw output:\n", response_text)

        match = re.search(r"\[.*?\]", response_text, re.DOTALL)
        sensitive_items = json.loads(match.group()) if match else []

        print("\n🔐 Sensitive items detected:", sensitive_items)

        for item in sensitive_items:
            if item in masked_text:
                encrypted = encrypt_text(item)
                masked_text = re.sub(re.escape(item), "***SENSITIVE***", masked_text)
                log.append({
                    "original": item,
                    "masked": "***SENSITIVE***",
                    "encrypted": encrypted
                })

                # ✅ Auto-learn logic
                if not any(item in ex for ex in examples):
                    label_guess = "sensitive value"
                    for prefix in ["PAN", "Aadhaar", "email", "phone", "ID", "account", "UPI", "license", "customer"]:
                        if prefix.lower() in text.lower():
                            label_guess = prefix
                            break

                    example_sentence = f"My {label_guess} is {item}"
                    add_example_to_vector_db(example_sentence)

    except Exception as e:
        print("⚠️ Gemini error:", e)

    return {
        "secured_text": masked_text,
        "log": log
    }
