import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def initialize_database():
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()

        # Create database and tables
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")

        # Create tables
        tables = {
            'users': """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(256) NOT NULL,
                    profile_image VARCHAR(255) DEFAULT 'default.png',
                    bio TEXT,
                    security_score INT DEFAULT 0,
                    job_title VARCHAR(100),
                    organization VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """,
            'quiz_results': """
                CREATE TABLE IF NOT EXISTS quiz_results (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    quiz_name VARCHAR(100),
                    score INT,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """,
            'user_activity': """
                CREATE TABLE IF NOT EXISTS user_activity (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    activity_type ENUM('quiz', 'video', 'article', 'case_study'),
                    activity_id VARCHAR(100),
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """,
            'notifications': """
                CREATE TABLE IF NOT EXISTS notifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    title VARCHAR(100),
                    message TEXT,
                    read_status BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """
        }

        for table_name, table_sql in tables.items():
            cursor.execute(table_sql)

        # Check if we need to alter the users table to add new columns
        cursor.execute("SHOW COLUMNS FROM users")
        existing_columns = [column[0] for column in cursor.fetchall()]
        
        # Add missing columns if they don't exist
        if 'profile_image' not in existing_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN profile_image VARCHAR(255) DEFAULT 'default.png'")
        
        if 'bio' not in existing_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN bio TEXT")
        
        if 'security_score' not in existing_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN security_score INT DEFAULT 0")
        
        if 'job_title' not in existing_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN job_title VARCHAR(100)")
        
        if 'organization' not in existing_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN organization VARCHAR(100)")

        conn.commit()
        print("Database and tables created successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
