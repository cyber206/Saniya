from src.Confrig import groq_api_key
from src.LLM import LLM
from src.Prompts import *
from src.Database import Database
import json
class Chatbot:
    def __init__(self):
        self.LLM = LLM(api_key=groq_api_key)
        self.database = Database()
        self.database.connect()
        self.database.create_tables()
        self.database.create_memories()

    def chat(self,user_input):
        self.database.save_messages(
            conversation_id = 1,
            role = "user",
            content = user_input,
        )
        history = self.database.get_messages(
            conversation_id = 1,
        )
        memory = self.database.get_memory(
            conversation_id = 1,
        )
        memory_text = ""
        for item in memory:
            memory_text += item["content"]
        messages = [
            {
                "role":"system",
                "content":SYSTEM_PROMPT + "User_memories" + memory_text,
            },
        ]
        messages.extend(history)
        response = self.LLM.generate(messages)
        self.database.save_messages(
            conversation_id = 1,
            role = "system",
            content = response,
        )
        self.extract_chat(user_input,response)
        return response

    def extract_chat(self,user_input,response):
        memory = [{
            "role":"system",
            "content":MEMORY_PROMPT

        },
            {
                "role":"user",
                "content":user_input,
            },
            {
                "role":"assistant",
                "content" : response,
            }
        ]
        response = self.LLM.generate(memory)
        start = response.find("[")
        end = response.rfind("]")+1
        response = response[start:end]
        memories = json.loads(response)
        for item in memories:
            memory=item["memory"]
            if not self.database.memory_exists(2,memory):
                self.database.save_memory(
                    conversation_id = 2,
                    memory = memory
                )

        return memories





