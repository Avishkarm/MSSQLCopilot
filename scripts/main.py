from llm import llm_decide, chat_only
from job_queries import get_failed_jobs, get_running_jobs

def format_jobs(rows):
    if not rows:
        return "No records found."

    output = []
    for r in rows:
        output.append(" | ".join(str(col) for col in r))
    return "\n".join(output)


while True:
    user_prompt = input("\nAsk about SQL Agent Jobs: ")

    decision = llm_decide(user_prompt)

    if decision["action"] == "sql_agent_jobs":
        job_type = decision.get("job_type")
        limit = decision.get("limit", 5)

        if job_type == "failed_jobs":
            rows = get_failed_jobs(limit)
            print(format_jobs(rows))

        elif job_type == "running_jobs":
            rows = get_running_jobs()
            print(format_jobs(rows))

        else:
            print("Job type not supported yet")

    else:
        print(chat_only(user_prompt))
