import ollama
import json
import re

SYSTEM_PROMPT = """
You are an AI router for Microsoft SQL Server SQL Agent Jobs.

Your task:
- Decide whether the user is asking about SQL Agent Jobs
- Or just general conversation

SQL Agent Job topics include:
- job status
- failed jobs
- running jobs
- job history
- schedules
- last run
- next run
- disabled jobs

Rules:
- You MUST respond with ONLY valid JSON
- No explanations
- No markdown
- No extra text

Valid responses ONLY:

{"action":"sql_agent_jobs","limit":5}
{"action":"chat","limit":0}
"""

def extract_json(text):
    """
    Extract the first JSON object from LLM output
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in LLM response: {text}")
    return match.group(0)


# # def llm_decide(user_prompt):
# #     response = ollama.chat(
# #         model="llama3.2:1b",
# #         messages=[
# #             {"role": "system", "content": SYSTEM_PROMPT},
# #             {"role": "user", "content": user_prompt}
# #         ]
# #     )

#     raw_output = response["message"]["content"]
#     print("\n[DEBUG] LLM raw output:\n", raw_output)

#     try:
#         json_text = extract_json(raw_output)
#         return json.loads(json_text)
#     except Exception:
#         print("[WARN] JSON parse failed, defaulting to chat mode")
#         return {"action": "chat", "limit": 0}

def llm_decide(user_prompt):
    response = ollama.chat(
        model="llama3.2:1b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    raw_output = response["message"]["content"]
    print("\n[DEBUG] LLM raw output:\n", raw_output)

    try:
        json_text = extract_json(raw_output)
        decision = json.loads(json_text)

        # 🔐 HARD GUARD
        if "action" not in decision:
            raise ValueError("Missing action key")

        return decision

    except Exception as e:
        print("[WARN] Invalid router response, fallback to chat")
        return {"action": "chat", "limit": 0}


def chat_only(user_prompt):
    response = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "user", "content": user_prompt}]
    )
    return response["message"]["content"]
