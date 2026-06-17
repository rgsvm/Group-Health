from openai import OpenAI

client = OpenAI()

def generate_summary(metrics: dict) -> str:
    prompt = f"""
You are a health data assistant.
Summarize these sleep metrics in simple language:
{metrics}

Give:
1. One-line summary
2. Main likely reason
3. One practical recommendation
"""
    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return resp.output_text
