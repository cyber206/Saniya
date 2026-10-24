from dotenv import load_dotenv
load_dotenv()
import os
groq_api_key = os.getenv("GROQ_API_KEY")
DB_NAME = "History"
DB_USER = "postgres"
DB_PASSWORD = "aman"
DB_HOST = "Localhost"
DB_PORT = 5432


