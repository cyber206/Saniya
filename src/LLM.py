from groq import Groq
class LLM:
    def __init__(self,api_key):
        self.client = Groq(api_key = api_key)

    def generate(self,messages):
        chat_completion = self.client.chat.completions.create(messages = messages,model = "openai/gpt-oss-120b")
        return chat_completion.choices[0].message.content


