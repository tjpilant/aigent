import sqlite3
from .utils.logger import get_logger

logger = get_logger(__name__)

def init_database():
    logger.info("Initializing database")
    try:
        conn = sqlite3.connect('agent_descriptors.db')
        cursor = conn.cursor()

        # Create the agent_descriptors table
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
        logger.debug("agent_descriptors table created successfully")

        # Insert some sample data
        sample_data = [
            ('NLP Developer', 'Develop NLP models, preprocess data', 'Handling ambiguous language', 'Sentiment analysis project',
             'tokenization, embeddings', 'Improve model accuracy', 'Data scientists, software engineers',
             'Technical and precise', 'Detailed explanations', 'Research papers, documentation',
             'Think of words as building blocks', 'Respond within 24 hours', 'Collaborative and open to feedback',
             'What specific NLP task are you working on?'),
            ('Data Scientist', 'Analyze data, create models', 'Dealing with large datasets', 'Customer churn prediction',
             'regression, classification', 'Extract actionable insights', 'Business analysts, software engineers',
             'Analytical and clear', 'In-depth analysis with visualizations', 'Academic journals, industry reports',
             'Data is like a puzzle to solve', 'Timely responses to queries', 'Works well in cross-functional teams',
             'What is the business objective of your analysis?')
        ]

        cursor.executemany('''
        INSERT OR REPLACE INTO agent_descriptors 
        (profession, key_responsibilities, typical_challenges, current_projects,
        jargon_terminology, goals_objectives, interactions, tone_formality,
        level_of_detail, preferred_references, examples_analogies, promptness,
        collaborative_approach, follow_up_questions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_data)
        logger.debug(f"Inserted {len(sample_data)} sample records into agent_descriptors table")

        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"An error occurred while initializing the database: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    init_database()
