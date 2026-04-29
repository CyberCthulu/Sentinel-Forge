# app/agent/agent.py

import json
import os
from openai import OpenAI

SYSTEM_PROMPT = """
You are a cyber-physical threat analyst.

Your job:
- Interpret structured incident data
- Provide clear, actionable guidance
- Be concise and decisive
- No fluff

Return JSON only:
{
  "assessment": "...",
  "priority": "...",
  "next_steps": ["...", "..."],
  "operator_note": "..."
}
"""


def run_agent(context: dict):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(context)},
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content

        if not content:
            return None

        return json.loads(content)

    except Exception as e:
        print(f"[AGENT ERROR] {e}")
        return None