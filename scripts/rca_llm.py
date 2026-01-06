import ollama

RCA_SYSTEM_PROMPT = """
You are a Senior SQL Server DBA.

Analyze SQL Agent Job failure messages and provide:
1. Root cause
2. Likely impact
3. Recommended fix
4. Preventive actions

Rules:
- Be concise
- Be technical but clear
- Do NOT hallucinate logs
- Base reasoning ONLY on the given error message
"""

def analyze_failure(job_name, step_name, error_message):
    user_prompt = f"""
Job Name: {job_name}
Step Name: {step_name}
Error Message:
{error_message}
"""

    response = ollama.chat(
        model="llama3.2:1b",
        messages=[
            {"role": "system", "content": RCA_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response["message"]["content"]
