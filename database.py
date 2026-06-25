import sqlite3

DB_NAME = "timeline.db"

def init_db():
    """Khởi tạo file database và bảng dữ liệu nếu chưa có"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tạo bảng lưu trữ cấu trúc tương tự Class Diagram
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT,
            gps_coords TEXT,
            encrypted_payload TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_media(file_path, gps_coords, encrypted_payload, status):
    """Chèn một bản ghi Media mới vào SQLite"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Media (file_path, gps_coords, encrypted_payload, status)
        VALUES (?, ?, ?, ?)
    ''', (file_path, gps_coords, encrypted_payload, status))
    conn.commit()
    conn.close()

def get_all_media():
    """Lấy toàn bộ danh sách để hiển thị lên Timeline"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Media ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows