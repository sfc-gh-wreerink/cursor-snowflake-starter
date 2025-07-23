from connector.snowflake_connection import get_connection

def run_query():
    conn = get_connection()
    try:
        cs = conn.cursor()
        cs.execute("SELECT CURRENT_TIMESTAMP();")
        print("Result:", cs.fetchone()[0])
    finally:
        cs.close()
        conn.close()

if __name__ == "__main__":
    run_query()
