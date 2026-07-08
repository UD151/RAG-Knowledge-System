import sqlite3
import uuid
from app.config.settings import settings


DB_PATH = settings.DB_PATH


# =========================
# 初始化数据库
# =========================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 开启 WAL（非常重要）
    cursor.execute("PRAGMA journal_mode=WAL")

    # session表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id TEXT PRIMARY KEY,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # message表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# =========================
# 创建会话
# =========================
def create_new_session():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    sid = str(uuid.uuid4())

    cursor.execute(
        "INSERT INTO chat_sessions (id, summary) VALUES (?, ?)",
        (sid, "新对话")
    )

    conn.commit()
    conn.close()

    return sid


# =========================
# 获取所有 session
# =========================
def get_all_sessions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, summary, created_at, updated_at
        FROM chat_sessions
        ORDER BY updated_at DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "summary": r[1],
            "created_at": r[2],
            "updated_at": r[3]
        }
        for r in data
    ]


# =========================
# 获取 messages
# =========================
def get_session_messages(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content, created_at
        FROM messages
        WHERE session_id = ?
        ORDER BY created_at ASC
    """, (session_id,))

    data = cursor.fetchall()
    conn.close()

    return [
        {
            "role": r[0],
            "content": r[1],
            "created_at": r[2]
        }
        for r in data
    ]


# =========================
# 保存消息
# =========================
def save_message_to_db(session_id: str, role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (session_id, role, content)
        VALUES (?, ?, ?)
    """, (session_id, role, content))

    # 更新 session summary
    if role == "user":
        cursor.execute("""
            UPDATE chat_sessions
            SET summary = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND summary = '新对话'
        """, (content[:20], session_id))
    else:
        cursor.execute("""
            UPDATE chat_sessions
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (session_id,))

    conn.commit()
    conn.close()


# =========================
# 删除 session
# =========================
def delete_session_and_messages(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM messages WHERE session_id=?", (session_id,))
        cursor.execute("DELETE FROM chat_sessions WHERE id=?", (session_id,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()