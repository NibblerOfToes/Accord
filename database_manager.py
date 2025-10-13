import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'database.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def validate_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def listExtension():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM users")
    results = cursor.fetchall()
    conn.close()
    return results

def get_user_contacts(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.name, m.text, m.date, m.time
        FROM messages m
        JOIN users u ON m.userID = u.userID
        WHERE m.userID = ?
        ORDER BY m.date DESC, m.time DESC
    """, (user_id,))
    contacts = cursor.fetchall()
    conn.close()
    return contacts

def get_contact_previews(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.name, m.text, m.userID
        FROM messages m
        JOIN users u ON m.userID = u.userID
        WHERE m.userID != ?
        AND EXISTS (
            SELECT 1 FROM messages m2
            WHERE m2.userID = m.userID AND m2.userID = ?
        )
        GROUP BY m.userID
        ORDER BY MAX(m.date || ' ' || m.time) DESC
    """, (user_id, user_id))
    contacts = cursor.fetchall()
    conn.close()
    return contacts

def get_messages_between(user_id, contact_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT text, userID FROM messages
        WHERE (userID = ? OR userID = ?)
        ORDER BY date, time
    """, (user_id, contact_id))
    messages = cursor.fetchall()
    conn.close()
    return messages

def get_user_name(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE userID = ?", (user_id,))
    name = cursor.fetchone()[0]
    conn.close()
    return name

def get_users_not_in_contacts(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT userID, name FROM users
        WHERE userID != ?
        AND userID NOT IN (
            SELECT contactID FROM contacts WHERE ownerID = ?
        )
        ORDER BY name
    """, (user_id, user_id))
    users = cursor.fetchall()
    conn.close()
    return users

def find_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT userID, name FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_user_contacts_with_preview(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.userID, u.name,
               (
                 SELECT text
                 FROM messages
                 WHERE (userID = ? AND receiverID = u.userID)
                    OR (userID = u.userID AND receiverID = ?)
                 ORDER BY date DESC, time DESC
                 LIMIT 1
               ) AS preview
        FROM users u
        WHERE u.userID != ?
        AND (
            u.userID IN (SELECT contactID FROM contacts WHERE ownerID = ?)
            OR u.userID IN (SELECT ownerID FROM contacts WHERE contactID = ?)
        )
        ORDER BY u.name
    """, (user_id, user_id, user_id, user_id, user_id))
    contacts = cursor.fetchall()
    conn.close()
    return contacts

def get_message_history(user_id, contact_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT text, userID, date, time
        FROM messages
        WHERE (userID = ? AND receiverID = ?)
           OR (userID = ? AND receiverID = ?)
        ORDER BY date, time
    """, (user_id, contact_id, contact_id, user_id))
    messages = cursor.fetchall()
    conn.close()
    return messages

def add_contact(owner_id, contact_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO contacts (ownerID, contactID)
        VALUES (?, ?)
    """, (owner_id, contact_id))
    conn.commit()
    conn.close()

def save_message(sender_id, receiver_id, text, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (userID, receiverID, text, date, time)
        VALUES (?, ?, ?, ?, ?)
    """, (
        sender_id,
        receiver_id,
        text,
        timestamp.strftime('%Y-%m-%d'),
        timestamp.strftime('%H:%M:%S')
    ))
    conn.commit()
    conn.close()

def get_group_timetable(group_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT day, period, subject, location, startTime, endTime
        FROM timetable
        WHERE groupID = ?
        ORDER BY day, period
    """, (group_id,))
    schedule = cursor.fetchall()
    conn.close()
    return schedule

def get_user_group(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT groupID FROM users WHERE userID = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

from datetime import datetime

PERIOD_WINDOWS = {
    1: ('08:45', '09:40'),
    2: ('09:40', '10:35'),
    3: ('10:55', '11:50'),
    4: ('11:50', '12:45'),
    5: ('13:25', '14:20'),
    6: ('14:20', '15:15')
}

from datetime import datetime

def get_current_or_next_class(today_schedule):
    now = datetime.now().strftime('%H:%M')

    for entry in today_schedule:
        _, period, subject, location, start, end = entry
        if start <= now <= end:
            return {
                'subject': subject,
                'location': location,
                'time': start,
                'status': 'Now'
            }
        elif now < start:
            return {
                'subject': subject,
                'location': location,
                'time': start,
                'status': 'Next'
            }

    return None

def get_recent_received_messages(user_id, limit=3):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT u.name, m.text, m.date, m.time
        FROM messages m
        JOIN users u ON m.userID = u.userID
        WHERE m.receiverID = ?
        ORDER BY m.date DESC, m.time DESC
        LIMIT ?
    """
    cursor.execute(query, (user_id, limit))
    results = cursor.fetchall()

    conn.close()
    return results

def create_user(email, password, name, role, group_id=None, subject=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return False

    cursor.execute("""
        INSERT INTO users (email, password, name, role, groupID, subject)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (email, password, name, role, group_id, subject))

    conn.commit()
    conn.close()
    return True

def get_teacher_timetable(subject):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT day, period, subject, location, startTime, endTime
        FROM timetable
        WHERE subject = ?
        ORDER BY day, period
    """, (subject,))
    schedule = cursor.fetchall()
    conn.close()
    return schedule

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT userID, name, role, groupID, subject FROM users WHERE userID = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'userID': row[0],
            'name': row[1],
            'role': row[2],
            'groupID': row[3],
            'subject': row[4]
        }
    return None

def save_public_message(sender_id, group_id, text, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO public_messages (senderID, groupID, text, date, time)
        VALUES (?, ?, ?, ?, ?)
    """, (
        sender_id,
        group_id,
        text,
        timestamp.strftime('%Y-%m-%d'),
        timestamp.strftime('%H:%M:%S')
    ))
    conn.commit()
    conn.close()

def get_public_messages_for_group(group_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.name, p.text, p.date, p.time
        FROM public_messages p
        JOIN users u ON p.senderID = u.userID
        WHERE p.groupID = ?
        ORDER BY p.date DESC, p.time DESC
    """, (group_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages