import os
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Tải các biến môi trường từ file .env
load_dotenv()

# Lấy các biến môi trường
DATABASE_URL = os.getenv("DATABASE_URL")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")

# Kiểm tra xem các biến môi trường đã được thiết lập chưa
if not DATABASE_URL or not PUSHOVER_API_TOKEN:
    logging.error("Lỗi: Vui lòng thiết lập DATABASE_URL và PUSHOVER_API_TOKEN trong file .env")
    exit(1)

# Thiết lập kết nối database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def send_pushover_notification(user_key, message):
    """Hàm gửi thông báo qua API của Pushover."""
    try:
        response = requests.post("https://api.pushover.net/1/messages.json", data={
            "token": PUSHOVER_API_TOKEN,
            "user": user_key,
            "message": message,
            "title": "Nhắc nhở mục tiêu!"
        })
        response.raise_for_status() # Báo lỗi nếu request thất bại (status code không phải 2xx)
        logging.info(f"Đã gửi thông báo thành công đến user_key: {user_key[:5]}...")
    except requests.exceptions.RequestException as e:
        logging.error(f"Lỗi khi gửi thông báo đến {user_key[:5]}...: {e}")

def main():
    """Hàm chính để tìm và gửi thông báo."""
    logging.info("Bắt đầu chạy worker nhắc nhở...")
    db = SessionLocal()
    try:
        # Câu lệnh SQL để lấy tất cả người dùng và các mục tiêu chưa hoàn thành của họ
        # Chúng ta dùng SQL thuần ở đây để có thể gom nhóm mục tiêu dễ dàng
        query = text("""
            SELECT u.pushover_user_key, STRING_AGG(g.content, '\n- ')
            FROM users u
            JOIN goals g ON u.id = g.owner_id
            WHERE g.status = 'pending' AND u.pushover_user_key IS NOT NULL
            GROUP BY u.pushover_user_key
        """)
        
        results = db.execute(query).fetchall()
        
        if not results:
            logging.info("Không tìm thấy mục tiêu nào cần nhắc nhở.")
            return

        logging.info(f"Tìm thấy {len(results)} người dùng có mục tiêu cần nhắc nhở.")

        for user_key, goals_content in results:
            message = f"Đừng quên các mục tiêu hôm nay nhé:\n- {goals_content}"
            send_pushover_notification(user_key, message)
            
    finally:
        db.close()
        logging.info("Worker đã chạy xong.")

if __name__ == "__main__":
    main()
