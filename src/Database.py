from src.Confrig import *
import psycopg

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = psycopg.connect(
            host=DB_HOST,
            user=DB_USER,
            password =DB_PASSWORD,
            dbname=DB_NAME,
            port=DB_PORT

        )
        print("Connection established with the Database.")


    def create_tables(self):
        with self.connection.cursor() as cursor:

            cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            conversation_id INTEGER NOT NULL,
            role varchar(20) NOT NULL,
            content TEXT NOT NULL
            );
            """

        )
            self.connection.commit()
        print("Tables created successfully.")

    def save_messages(self,conversation_id,role,content):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO messages (conversation_id, role, content)
                VALUES (%s, %s, %s)
                """,(conversation_id,role,content)
            )
            self.connection.commit()


    def get_messages(self,conversation_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT  role,content
                FROM messages
                WHERE conversation_id = %s
                ORDER BY id
                """,(conversation_id,))

            rows = cursor.fetchall()

            memories = []
            for row in rows:
                memories.append({
                    "role":row[0],
                    "content":row[1],
                })
            return memories

    def create_memories(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories(
            id SERIAL PRIMARY KEY,
            conversation_id INTEGER NOT NULL,
            memory TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """)

            self.connection.commit()
        print("Memories successfully created")


    def save_memory(self, conversation_id,memory):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO memories(conversation_id, memory)
            VALUES (%s, %s)
            """,(conversation_id, memory))

            self.connection.commit()


    def get_memory(self,conversation_id):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            SELECT memory,conversation_id
            FROM memories
            WHERE conversation_id = %s
            ORDER BY id
            """,(conversation_id,))

            rows = cursor.fetchall()
            memories = []
            for row in rows:
                memories.append({
                    "memory": row[0],
                })
            return memories


    def memory_exists(self,conversation_id,memory):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 1
                FROM memories
                WHERE conversation_id = %s
                AND memory = %s
                LIMIT 1
                """,(conversation_id,memory)
            )
            exists = cursor.fetchone() is not None

        return exists

