import sqlite3
import logging

def init_database():
    try:
        conn = sqlite3.connect('agent_descriptors.db')
        cursor = conn.cursor()
        
        # Create table for agent descriptors if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_descriptors (
                id INTEGER PRIMARY KEY,
                profession TEXT UNIQUE,
                key_responsibilities TEXT,
                typical_challenges TEXT,
                current_projects TEXT,
                jargon_terminology TEXT,
                goals_objectives TEXT,
                interactions TEXT,
                tone_formality TEXT,
                level_of_detail TEXT,
                preferred_references TEXT,
                examples_analogies TEXT,
                promptness TEXT,
                collaborative_approach TEXT,
                follow_up_questions TEXT
            )
        ''')
        
        conn.commit()
        logging.info("Database initialized successfully")
    except sqlite3.Error as e:
        logging.error(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_database()