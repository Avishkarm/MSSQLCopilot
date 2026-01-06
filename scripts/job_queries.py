from conn import create_connection

def get_failed_jobs(limit=5):
    query = f"""
    SELECT TOP {limit}
        j.name AS JobName,
        h.step_name,
        h.run_date,
        h.run_time,
        h.message
    FROM msdb.dbo.sysjobhistory h
    JOIN msdb.dbo.sysjobs j ON h.job_id = j.job_id
    WHERE h.run_status = 0
      AND h.step_id <> 0
    ORDER BY h.run_date DESC, h.run_time DESC
    """

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return rows



def get_running_jobs():
    query = """
    SELECT
        j.name AS JobName,
        a.start_execution_date
    FROM msdb.dbo.sysjobs j
    JOIN msdb.dbo.sysjobactivity a ON j.job_id = a.job_id
    WHERE a.stop_execution_date IS NULL
    """

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return rows


