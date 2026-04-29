import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    # Ensure instance directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Event:
    @staticmethod
    def create(title, description, event_date, location, capacity):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO event (title, description, event_date, location, capacity)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, description, event_date, location, capacity))
        conn.commit()
        event_id = cursor.lastrowid
        conn.close()
        return event_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        events = conn.execute('SELECT * FROM event ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(e) for e in events]

    @staticmethod
    def get_by_id(event_id):
        conn = get_db_connection()
        event = conn.execute('SELECT * FROM event WHERE id = ?', (event_id,)).fetchone()
        conn.close()
        return dict(event) if event else None

    @staticmethod
    def update(event_id, title, description, event_date, location, capacity):
        conn = get_db_connection()
        conn.execute('''
            UPDATE event 
            SET title = ?, description = ?, event_date = ?, location = ?, capacity = ?
            WHERE id = ?
        ''', (title, description, event_date, location, capacity, event_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(event_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM event WHERE id = ?', (event_id,))
        conn.commit()
        conn.close()


class Registration:
    @staticmethod
    def create(event_id, student_id, name, phone):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Checking event capacity to determine status
        event = conn.execute('SELECT capacity FROM event WHERE id = ?', (event_id,)).fetchone()
        if not event:
            conn.close()
            return None, "Event not found"
            
        capacity = event['capacity']
        
        current_registrations = conn.execute(
            'SELECT COUNT(*) as count FROM registration WHERE event_id = ? AND status = ?', 
            (event_id, '成功')
        ).fetchone()
        
        if current_registrations['count'] < capacity:
            status = '成功'
        else:
            status = '候補中'
            
        cursor.execute('''
            INSERT INTO registration (event_id, student_id, name, phone, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (event_id, student_id, name, phone, status))
        
        conn.commit()
        reg_id = cursor.lastrowid
        conn.close()
        return reg_id, status

    @staticmethod
    def get_all():
        conn = get_db_connection()
        registrations = conn.execute('SELECT * FROM registration ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(r) for r in registrations]

    @staticmethod
    def get_by_id(reg_id):
        conn = get_db_connection()
        registration = conn.execute('SELECT * FROM registration WHERE id = ?', (reg_id,)).fetchone()
        conn.close()
        return dict(registration) if registration else None

    @staticmethod
    def get_by_student(student_id):
        conn = get_db_connection()
        # Join with event to get event title
        registrations = conn.execute('''
            SELECT r.*, e.title as event_title 
            FROM registration r
            JOIN event e ON r.event_id = e.id
            WHERE r.student_id = ? 
            ORDER BY r.created_at DESC
        ''', (student_id,)).fetchall()
        conn.close()
        return [dict(r) for r in registrations]

    @staticmethod
    def update_status(reg_id, status):
        conn = get_db_connection()
        conn.execute('UPDATE registration SET status = ? WHERE id = ?', (status, reg_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(reg_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM registration WHERE id = ?', (reg_id,))
        conn.commit()
        conn.close()
