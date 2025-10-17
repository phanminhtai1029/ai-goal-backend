import psycopg2

try:
    conn = psycopg2.connect(
        dbname="goal_assistant",
        user="tai_user",
        password="Tai03062005@",
        host="localhost",
        port="5432"
    )
    print("✅ Connected Successfully!")
    conn.close()
except Exception as e:
    print("❌ Lỗi:", e)
