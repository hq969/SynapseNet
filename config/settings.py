import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    PG_CONNECTION = os.getenv(
        "POSTGRES_CONNECTION_STRING", 
        "postgresql://admin:password@localhost:5432/synapsenet"
    )

settings = Settings()
